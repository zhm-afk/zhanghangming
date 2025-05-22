from flask import Blueprint, request, jsonify
from app.services.admin_service import AdminService
from app.utils.auth import admin_required, super_admin_required

# 创建蓝图
admins_bp = Blueprint('admins', __name__)

@admins_bp.route('/', methods=['GET'])
@admin_required
def get_all_admins():
    """获取所有管理员列表"""
    admins = AdminService.get_all_admins()
    return jsonify({
        'success': True,
        'data': [admin.to_dict() for admin in admins]
    })

@admins_bp.route('/<int:admin_id>', methods=['GET'])
@admin_required
def get_admin(admin_id):
    """获取单个管理员信息"""
    admin = AdminService.get_admin_by_id(admin_id)
    if not admin:
        return jsonify({
            'success': False,
            'message': '管理员不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': admin.to_dict()
    })

@admins_bp.route('/', methods=['POST'])
@super_admin_required
def create_admin():
    """创建新管理员（仅超级管理员可操作）"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    # 检查必要字段
    if not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': '用户名和密码不能为空'
        }), 400
    
    # 检查用户名是否已存在
    existing_admin = AdminService.get_admin_by_username(data.get('username'))
    if existing_admin:
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        }), 409
    
    # 创建管理员
    admin = AdminService.create_admin(data)
    return jsonify({
        'success': True,
        'message': '管理员创建成功',
        'data': admin.to_dict()
    }), 201

@admins_bp.route('/<int:admin_id>', methods=['PUT'])
@super_admin_required
def update_admin(admin_id):
    """更新管理员信息（仅超级管理员可操作）"""
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    admin = AdminService.update_admin(admin_id, data)
    if not admin:
        return jsonify({
            'success': False,
            'message': '管理员不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '管理员更新成功',
        'data': admin.to_dict()
    })

@admins_bp.route('/<int:admin_id>', methods=['DELETE'])
@super_admin_required
def delete_admin(admin_id):
    """删除管理员（仅超级管理员可操作）"""
    success = AdminService.delete_admin(admin_id)
    if not success:
        return jsonify({
            'success': False,
            'message': '管理员不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'message': '管理员删除成功'
    }) 