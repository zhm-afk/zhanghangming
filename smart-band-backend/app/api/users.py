from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.utils.auth import token_required

# 创建蓝图
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@token_required
def get_all_users():
    """获取所有用户列表"""
    users = UserService.get_all_users()
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users]
    })

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """获取单个用户信息"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    })

@users_bp.route('/', methods=['POST'])
@token_required
def create_user():
    """创建新用户"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    # 检查用户名是否已存在
    existing_user = UserService.get_user_by_username(data.get('username'))
    if existing_user:
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        }), 409
    
    # 检查设备ID是否已存在
    if 'deviceId' in data:
        existing_device = UserService.get_user_by_device_id(data.get('deviceId'))
        if existing_device:
            return jsonify({
                'success': False,
                'message': '设备ID已存在'
            }), 409
    
    # 创建用户
    user = UserService.create_user(data)
    return jsonify({
        'success': True,
        'message': '用户创建成功',
        'data': user.to_dict()
    }), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """更新用户信息"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    user = UserService.update_user(user_id, data)
    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '用户更新成功',
        'data': user.to_dict()
    })

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """删除用户"""
    success = UserService.delete_user(user_id)
    if not success:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '用户删除成功'
    })

@users_bp.route('/health/<string:username>', methods=['GET'])
@token_required
def get_user_health(username):
    """获取用户健康数据"""
    health_data = UserService.get_user_health_data(username)
    if not health_data:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': health_data
    })

@users_bp.route('/location/<string:username>', methods=['GET'])
@token_required
def get_user_location(username):
    """获取用户位置数据"""
    location_data = UserService.get_user_location(username)
    if not location_data:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': location_data
    })

@users_bp.route('/stats/heart-rate', methods=['GET'])
@token_required
def get_average_heart_rate():
    """获取所有用户的平均心率"""
    avg_heart_rate = UserService.calculate_average_heart_rate()
    return jsonify({
        'success': True,
        'data': avg_heart_rate
    })

@users_bp.route('/stats/blood-pressure', methods=['GET'])
@token_required
def get_average_blood_pressure():
    """获取所有用户的平均血压"""
    avg_blood_pressure = UserService.calculate_average_blood_pressure()
    return jsonify({
        'success': True,
        'data': avg_blood_pressure
    })

@users_bp.route('/stats/steps', methods=['GET'])
@token_required
def get_average_steps():
    """获取所有用户的平均步数"""
    avg_steps = UserService.calculate_average_steps()
    return jsonify({
        'success': True,
        'data': avg_steps
    })

@users_bp.route('/stats/heart-rate-distribution', methods=['GET'])
@token_required
def get_heart_rate_distribution():
    """获取心率分布"""
    distribution = UserService.get_heart_rate_distribution()
    return jsonify({
        'success': True,
        'data': distribution
    })
