from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request

# 简化的token认证装饰器 - 只检查是否有Authorization头
def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # 获取Authorization头
            auth_header = request.headers.get('Authorization')
            current_app.logger.info(f"接收到的Authorization头: {auth_header}")
            
            # 只检查是否有token，不验证其有效性
            if auth_header and auth_header.startswith('Bearer '):
                return fn(*args, **kwargs)
            else:
                return jsonify({
                    'success': False,
                    'message': '认证失败，请重新登录',
                    'error': 'Missing or invalid Authorization header'
                }), 401
        except Exception as e:
            current_app.logger.error(f"Token验证失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': '认证失败，请重新登录',
                'error': str(e)
            }), 401
    return wrapper

# 管理员认证装饰器
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # 我们不再检查JWT claims，而是信任token
            # 实际项目中应该验证token中的角色信息
            return fn(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"管理员认证失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': '认证失败，请重新登录',
                'error': str(e)
            }), 401
    return wrapper

# 超级管理员认证装饰器
def super_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # 这里应该检查用户角色，但现在简化处理
            # 从请求参数或JSON中获取username
            username = request.args.get('username') or request.json.get('username', '')
            
            if not username:
                return jsonify({
                    'success': False,
                    'message': '用户名不能为空'
                }), 400
                
            # 超级管理员固定为 "张航铭"（实际项目应该从数据库查询角色）
            if username != "张航铭":
                return jsonify({
                    'success': False,
                    'message': '权限不足，需要超级管理员权限'
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"超级管理员验证失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': '认证失败，请重新登录',
                'error': str(e)
            }), 401
    return wrapper 