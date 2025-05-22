from flask import Blueprint, request, jsonify
from app.services.smart_band_user_service import SmartBandUserService
from app.utils.auth import token_required

# 创建蓝图
smart_band_users_bp = Blueprint('smart_band_users', __name__)

@smart_band_users_bp.route('/', methods=['GET'])
@token_required
def get_all_users():
    """获取所有智能手环用户列表"""
    users = SmartBandUserService.get_all_users()
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users]
    })

@smart_band_users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """获取单个智能手环用户信息"""
    user = SmartBandUserService.get_user_by_id(user_id)
    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    })

@smart_band_users_bp.route('/', methods=['POST'])
@token_required
def create_user():
    """创建新智能手环用户"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    # 检查用户名是否已存在
    existing_user = SmartBandUserService.get_user_by_username(data.get('username'))
    if existing_user:
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        }), 409
    
    # 检查设备ID是否已存在
    if 'deviceId' in data:
        existing_device = SmartBandUserService.get_user_by_device_id(data.get('deviceId'))
        if existing_device:
            return jsonify({
                'success': False,
                'message': '设备ID已存在'
            }), 409
    
    # 创建用户
    user = SmartBandUserService.create_user(data)
    return jsonify({
        'success': True,
        'message': '用户创建成功',
        'data': user.to_dict()
    }), 201

@smart_band_users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """更新智能手环用户信息"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    user = SmartBandUserService.update_user(user_id, data)
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

@smart_band_users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """删除智能手环用户"""
    success = SmartBandUserService.delete_user(user_id)
    if not success:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '用户删除成功'
    }) 