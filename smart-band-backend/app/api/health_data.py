from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.health_data import HealthData
from app.models.device import Device
from app.models.customer import Customer
from app.extensions import db

health_data_bp = Blueprint('health_data', __name__)

@health_data_bp.route('/', methods=['GET'])
@jwt_required()
def get_health_data():
    """获取健康数据列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    customer_id = request.args.get('customer_id', type=int)
    device_id = request.args.get('device_id', type=int)
    
    query = HealthData.query
    
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    
    if device_id:
        query = query.filter_by(device_id=device_id)
    
    health_data = query.order_by(HealthData.timestamp.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': {
            'health_data': [{
                'id': data.id,
                'customer_id': data.customer_id,
                'device_id': data.device_id,
                'timestamp': data.timestamp.isoformat() if data.timestamp else None,
                'heart_rate': data.heart_rate,
                'systolic_pressure': data.systolic_pressure,
                'diastolic_pressure': data.diastolic_pressure,
                'steps': data.steps,
                'calories': data.calories,
                'sleep_duration': data.sleep_duration,
                'oxygen_saturation': data.oxygen_saturation,
                'temperature': data.temperature,
                'environment_temperature': data.environment_temperature,
                'humidity': data.humidity,
                'pressure': data.pressure
            } for data in health_data.items],
            'total': health_data.total,
            'pages': health_data.pages,
            'current_page': health_data.page
        }
    })

@health_data_bp.route('/customer/<int:customer_id>/summary', methods=['GET'])
@jwt_required()
def get_customer_health_summary(customer_id):
    """获取客户健康数据概要"""
    # 检查客户是否存在
    customer = Customer.query.get_or_404(customer_id)
    
    # 获取时间范围参数
    days = request.args.get('days', 7, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 查询最新心率
    latest_health_data = HealthData.query.filter_by(customer_id=customer_id)\
        .order_by(HealthData.timestamp.desc()).first()
    
    # 计算心率平均值
    avg_heart_rate = db.session.query(func.avg(HealthData.heart_rate))\
        .filter(HealthData.customer_id == customer_id,
                HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 计算步数总计
    total_steps = db.session.query(func.sum(HealthData.steps))\
        .filter(HealthData.customer_id == customer_id,
                HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 计算卡路里总计
    total_calories = db.session.query(func.sum(HealthData.calories))\
        .filter(HealthData.customer_id == customer_id,
                HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 计算睡眠时长
    total_sleep = db.session.query(func.sum(HealthData.sleep_duration))\
        .filter(HealthData.customer_id == customer_id,
                HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date,
                HealthData.sleep_duration != None)\
        .scalar()
    
    # 按天分组计算每日数据
    daily_data = db.session.query(
            func.date(HealthData.timestamp).label('date'),
            func.avg(HealthData.heart_rate).label('avg_heart_rate'),
            func.sum(HealthData.steps).label('steps'),
            func.sum(HealthData.calories).label('calories'),
            func.sum(HealthData.sleep_duration).label('sleep')
        )\
        .filter(HealthData.customer_id == customer_id,
                HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .group_by(func.date(HealthData.timestamp))\
        .all()
    
    return jsonify({
        'success': True,
        'data': {
            'customer_id': customer_id,
            'customer_name': customer.nickname,
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'current': {
                'heart_rate': latest_health_data.heart_rate if latest_health_data else None,
                'systolic_pressure': latest_health_data.systolic_pressure if latest_health_data else None,
                'diastolic_pressure': latest_health_data.diastolic_pressure if latest_health_data else None,
                'oxygen_saturation': latest_health_data.oxygen_saturation if latest_health_data else None,
                'temperature': latest_health_data.temperature if latest_health_data else None,
                'timestamp': latest_health_data.timestamp.isoformat() if latest_health_data and latest_health_data.timestamp else None
            },
            'summary': {
                'avg_heart_rate': round(avg_heart_rate, 1) if avg_heart_rate else 0,
                'total_steps': int(total_steps) if total_steps else 0,
                'total_calories': round(total_calories, 1) if total_calories else 0,
                'total_sleep_minutes': int(total_sleep) if total_sleep else 0,
                'avg_daily_steps': int(total_steps / days) if total_steps else 0,
                'avg_daily_sleep_minutes': int(total_sleep / days) if total_sleep else 0
            },
            'daily_data': [{
                'date': str(item.date),
                'avg_heart_rate': round(item.avg_heart_rate, 1) if item.avg_heart_rate else 0,
                'steps': int(item.steps) if item.steps else 0,
                'calories': round(item.calories, 1) if item.calories else 0,
                'sleep_minutes': int(item.sleep) if item.sleep else 0
            } for item in daily_data]
        }
    })

@health_data_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_health_statistics():
    """获取健康数据统计信息"""
    days = request.args.get('days', 7, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 获取总健康数据量
    total_records = HealthData.query.filter(
        HealthData.timestamp >= start_date,
        HealthData.timestamp <= end_date
    ).count()
    
    # 获取平均心率
    avg_heart_rate = db.session.query(func.avg(HealthData.heart_rate))\
        .filter(HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 获取平均血压
    avg_systolic = db.session.query(func.avg(HealthData.systolic_pressure))\
        .filter(HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    avg_diastolic = db.session.query(func.avg(HealthData.diastolic_pressure))\
        .filter(HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 获取总步数
    total_steps = db.session.query(func.sum(HealthData.steps))\
        .filter(HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .scalar()
    
    # 按日期分组获取每日数据量
    daily_counts = db.session.query(
            func.date(HealthData.timestamp).label('date'),
            func.count().label('count')
        )\
        .filter(HealthData.timestamp >= start_date,
                HealthData.timestamp <= end_date)\
        .group_by(func.date(HealthData.timestamp))\
        .all()
    
    return jsonify({
        'success': True,
        'data': {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'statistics': {
                'total_records': total_records,
                'avg_heart_rate': round(avg_heart_rate, 1) if avg_heart_rate else 0,
                'avg_blood_pressure': {
                    'systolic': round(avg_systolic, 1) if avg_systolic else 0,
                    'diastolic': round(avg_diastolic, 1) if avg_diastolic else 0
                },
                'total_steps': int(total_steps) if total_steps else 0,
                'avg_daily_records': round(total_records / days, 1) if total_records else 0
            },
            'daily_data': [{
                'date': str(item.date),
                'record_count': item.count
            } for item in daily_counts]
        }
    })
