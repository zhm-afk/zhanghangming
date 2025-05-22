from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.device import Device
from app.models.health_data import HealthData
from app.extensions import db
from app.utils.realtime_simulator import start_simulator, stop_simulator, simulator

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    """获取所有设备列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = Device.query
    
    if status:
        query = query.filter_by(status=status)
    
    devices = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': {
            'devices': [{
                'id': device.id,
                'device_id': device.device_id,
                'device_name': device.device_name,
                'customer_id': device.customer_id,
                'status': device.status,
                'battery_level': device.battery_level,
                'firmware': device.firmware,
                'last_sync': device.last_sync.isoformat() if device.last_sync else None,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'area': device.area,
                'location_updated_at': device.location_updated_at.isoformat() if device.location_updated_at else None,
                'created_at': device.created_at.isoformat()
            } for device in devices.items],
            'total': devices.total,
            'pages': devices.pages,
            'current_page': devices.page
        }
    })

@devices_bp.route('/<int:device_id>', methods=['GET'])
@jwt_required()
def get_device(device_id):
    """获取单个设备详情"""
    device = Device.query.get_or_404(device_id)
    
    return jsonify({
        'success': True,
        'data': {
            'id': device.id,
            'device_id': device.device_id,
            'device_name': device.device_name,
            'customer_id': device.customer_id,
            'status': device.status,
            'battery_level': device.battery_level,
            'firmware': device.firmware,
            'last_sync': device.last_sync.isoformat() if device.last_sync else None,
            'latitude': device.latitude,
            'longitude': device.longitude,
            'area': device.area,
            'location_updated_at': device.location_updated_at.isoformat() if device.location_updated_at else None,
            'created_at': device.created_at.isoformat()
        }
    })

@devices_bp.route('/<int:device_id>/health-data', methods=['GET'])
@jwt_required()
def get_device_health_data(device_id):
    """获取设备健康数据"""
    device = Device.query.get_or_404(device_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    health_data = HealthData.query.filter_by(device_id=device_id)\
        .order_by(HealthData.timestamp.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': {
            'health_data': [{
                'id': data.id,
                'timestamp': data.timestamp.isoformat(),
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

@devices_bp.route('/simulator/status', methods=['GET'])
@jwt_required()
def get_simulator_status():
    """获取模拟器状态"""
    return jsonify({
        'success': True,
        'data': {
            'running': simulator.running,
            'active_devices': simulator.get_active_device_count() if simulator.running else 0
        }
    })

@devices_bp.route('/simulator/start', methods=['POST'])
@jwt_required()
def start_simulator_api():
    """启动模拟器"""
    success = start_simulator()
    
    return jsonify({
        'success': success,
        'message': '模拟器已启动' if success else '模拟器启动失败，可能已经在运行',
        'data': {
            'running': simulator.running,
            'active_devices': simulator.get_active_device_count() if simulator.running else 0
        }
    })

@devices_bp.route('/simulator/stop', methods=['POST'])
@jwt_required()
def stop_simulator_api():
    """停止模拟器"""
    success = stop_simulator()
    
    return jsonify({
        'success': success,
        'message': '模拟器已停止' if success else '模拟器停止失败，可能已经停止运行',
        'data': {
            'running': not success
        }
    })
