from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.admin_service import AdminService
from app.utils.auth import admin_required, token_required
from datetime import datetime, timedelta
from app.models.admin import Admin
from app import db

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
    data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'success': False,
                'message': '用户名和密码不能为空'
        }), 400
    
        admin = Admin.query.filter_by(username=username).first()
        if not admin or not admin.check_password(password):
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401
    
        # 创建包含角色信息的token
    access_token = create_access_token(
            identity=admin.id,
            additional_claims={
                'username': admin.username,
                'role': admin.role,
                'nickname': admin.nickname
            }
    )
    
    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': {
                'token': access_token,
                'admin': {
                    'id': admin.id,
                    'username': admin.username,
                    'nickname': admin.nickname,
                    'role': admin.role
                }
        }
    })
        
    except Exception as e:
        current_app.logger.error(f"登录失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '登录失败',
            'error': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """管理员登出"""
    current_user = get_jwt_identity()
    
    # 更新登出状态
    success = AdminService.logout_admin(current_user)
    if not success:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '登出成功'
    })

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    try:
        # 获取JWT中的用户信息
        claims = get_jwt()
        admin_id = get_jwt_identity()
        
        admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'success': True,
            'data': {
                'id': admin.id,
                'username': admin.username,
                'nickname': admin.nickname,
                'role': admin.role
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取用户信息失败',
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新当前登录管理员信息"""
    current_user = get_jwt_identity()
    admin = AdminService.get_admin_by_username(current_user)
    
    if not admin:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    # 防止普通管理员修改角色
    if 'role' in data and admin.role != 'super':
        return jsonify({
            'success': False,
            'message': '权限不足，无法修改角色'
        }), 403
    
    updated_admin = AdminService.update_admin(admin.id, data)
    return jsonify({
        'success': True,
        'message': '个人信息更新成功',
        'data': updated_admin.to_dict()
    })
