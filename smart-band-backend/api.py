from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import pymysql
import pymysql.cursors
import os
import datetime
import base64
import time
import uuid
import re
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.auth import token_required, admin_required, super_admin_required

# 确保头像存储目录存在
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
AVATAR_FOLDER = os.path.join(STATIC_FOLDER, 'avatars')
os.makedirs(AVATAR_FOLDER, exist_ok=True)
AVATAR_URL_PREFIX = '/static/avatars/'

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
CORS(app) # 启用CORS，允许前端跨域请求

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ailing@200930',
    'db': 'smart_band',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(**db_config)

# 用于处理Base64图片数据并保存到文件
def save_base64_image(base64_data, admin_id):
    """
    保存Base64编码的图片数据到文件
    - base64_data: Base64编码的图片数据
    - admin_id: 管理员ID，用于生成唯一文件名
    返回: 保存成功返回文件URL，否则返回None
    """
    try:
        # 检查数据格式
        if not base64_data or not base64_data.startswith('data:image/'):
            return None
            
        # 解析头部和数据
        header, encoded = base64_data.split(',', 1)
        file_ext = re.search(r'data:image/(\w+);', header).group(1)
        
        # 生成唯一文件名
        filename = f"avatar_{admin_id}_{int(time.time())}_{uuid.uuid4().hex[:8]}.{file_ext}"
        file_path = os.path.join(AVATAR_FOLDER, filename)
        
        # 解码并保存文件
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(encoded))
            
        return AVATAR_URL_PREFIX + filename
    except Exception as e:
        print(f"保存头像出错: {str(e)}")
        return None

# 管理员API接口
@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            admin = cursor.fetchone()
            
            if not admin or not check_password_hash(admin['password_hash'], password):
                return jsonify({
                    'success': False,
                    'message': '用户名或密码错误'
                }), 401
            
            # 更新管理员状态和最后登录时间
            now = datetime.datetime.now()
            cursor.execute(
                "UPDATE admins SET status = '在线', last_login = %s WHERE id = %s",
                (now, admin['id'])
            )
            connection.commit()
            
            # 返回管理员信息（不包含密码）
            admin_data = {
                'id': admin['id'],
                'username': admin['username'],
                'nickname': admin['nickname'],
                'role': admin['role'],
                'status': '在线',
                'lastLogin': now.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 生成一个简单的token（实际应该使用JWT）
            import hashlib
            import time
            token = hashlib.md5(f"{username}:{time.time()}".encode()).hexdigest()
            
            return jsonify({
                'success': True,
                'message': '登录成功',
                'data': {
                    'admin': admin_data,
                    'access_token': token
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/auth/logout', methods=['POST'])
def admin_logout():
    """管理员登出"""
    try:
        # 从请求头获取用户名（实际应该从token解析）
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': '未授权'
            }), 401
        
        # 简单处理，这里应该从token中获取用户名
        username = request.json.get('username', '')
        
        if not username:
            return jsonify({
                'success': False,
                'message': '用户名不能为空'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE admins SET status = '离线' WHERE username = %s",
                (username,)
            )
            connection.commit()
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 404
            
            return jsonify({
                'success': True,
                'message': '登出成功'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登出失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins', methods=['GET'])
@token_required
def get_all_admins():
    """获取所有管理员"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, nickname, role, status, last_login, avatar FROM admins")
            admins = cursor.fetchall()
            
            # 格式化管理员数据
            formatted_admins = []
            for admin in admins:
                formatted_admins.append({
                    'id': admin['id'],
                    'username': admin['username'],
                    'nickname': admin['nickname'],
                    'role': admin['role'],
                    'status': admin['status'],
                    'lastLogin': admin['last_login'].strftime('%Y-%m-%d %H:%M:%S') if admin['last_login'] else '从未登录',
                    'avatar': admin['avatar']
                })
            
            return jsonify({
                'success': True,
                'data': formatted_admins
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取管理员列表失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins/<int:admin_id>', methods=['GET'])
@token_required
def get_admin(admin_id):
    """获取单个管理员"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, nickname, role, status, last_login, avatar FROM admins WHERE id = %s",
                (admin_id,)
            )
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '管理员不存在'
                }), 404
            
            # 格式化管理员数据
            admin_data = {
                'id': admin['id'],
                'username': admin['username'],
                'nickname': admin['nickname'],
                'role': admin['role'],
                'status': admin['status'],
                'lastLogin': admin['last_login'].strftime('%Y-%m-%d %H:%M:%S') if admin['last_login'] else '从未登录',
                'avatar': admin['avatar']
            }
            
            return jsonify({
                'success': True,
                'data': admin_data
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取管理员信息失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins', methods=['POST'])
@token_required
@admin_required
def create_admin():
    """创建新管理员"""
    try:
        data = request.json
        
        # 检查必要字段
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT id FROM admins WHERE username = %s", (data['username'],))
            if cursor.fetchone():
                return jsonify({
                    'success': False,
                    'message': '用户名已存在'
                }), 409
            
            # 生成密码哈希
            password_hash = generate_password_hash(data['password'])
            
            # 创建新管理员
            sql = """
            INSERT INTO admins (
                username, nickname, password_hash, role
            ) VALUES (
                %s, %s, %s, %s
            )
            """
            
            nickname = data.get('nickname', data['username'])
            role = data.get('role', 'normal')
            
            cursor.execute(sql, (
                data['username'],
                nickname,
                password_hash,
                role
            ))
            connection.commit()
            
            new_id = cursor.lastrowid
            
            # 返回新创建的管理员
            return jsonify({
                'success': True,
                'message': '管理员创建成功',
                'data': {
                    'id': new_id,
                    'username': data['username'],
                    'nickname': nickname,
                    'role': role,
                    'status': '离线',
                    'lastLogin': '从未登录'
                }
            }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建管理员失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins/<int:admin_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_admin(admin_id):
    """删除管理员"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 检查管理员是否存在
            cursor.execute("SELECT username, role FROM admins WHERE id = %s", (admin_id,))
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '管理员不存在'
                }), 404
            
            # 防止删除超级管理员
            if admin['role'] == 'super':
                return jsonify({
                    'success': False,
                    'message': '不能删除超级管理员'
                }), 403
            
            # 删除管理员
            cursor.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f"成功删除管理员 {admin['username']}"
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除管理员失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """获取所有用户"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM smart_band_users")
            users = cursor.fetchall()
            
            # 将数据转换为前端需要的格式 - 简化版，只包含基本信息
            formatted_users = []
            for user in users:
                formatted_users.append({
                    'id': user['id'],
                    'username': user['username'],
                    'nickname': user['nickname'],
                    'age': user['age'],
                    'deviceId': user['device_id'],
                    'registerTime': user['register_time'].strftime('%Y-%m-%d') if user['register_time'] else None
                })
            
            return jsonify({
                'success': True,
                'data': formatted_users
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取用户数据失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户信息"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM smart_band_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 404
            
            # 将数据转换为前端需要的格式 - 简化版，只包含基本信息
            formatted_user = {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'age': user['age'],
                'deviceId': user['device_id'],
                'registerTime': user['register_time'].strftime('%Y-%m-%d') if user['register_time'] else None
            }
            
            return jsonify({
                'success': True,
                'data': formatted_user
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取用户数据失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 查询用户是否存在
            cursor.execute("SELECT username FROM smart_band_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 404
            
            # 删除用户
            cursor.execute("DELETE FROM smart_band_users WHERE id = %s", (user_id,))
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f"成功删除用户 {user['username']}"
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除用户失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建新用户"""
    try:
        data = request.json
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE username = %s", (data['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': f"用户 {data['username']} 已存在"
                }), 400
                
            # 获取当前最大ID
            cursor.execute("SELECT MAX(id) as max_id FROM smart_band_users")
            result = cursor.fetchone()
            new_id = 1
            if result['max_id']:
                new_id = result['max_id'] + 1
            
            # 如果没有提供设备ID或为空，生成一个唯一的设备ID
            device_id = data.get('deviceId', '')
            if not device_id:
                # 生成随机设备ID
                import random
                import time
                timestamp = str(int(time.time()))[-4:]
                random_num = str(random.randint(1000, 9999))
                device_id = f"SB{timestamp}{random_num}"
                
                # 确保生成的设备ID唯一
                is_unique = False
                retry_count = 0
                while not is_unique and retry_count < 10:
                    cursor.execute("SELECT id FROM smart_band_users WHERE device_id = %s", (device_id,))
                    if not cursor.fetchone():
                        is_unique = True
                    else:
                        random_num = str(random.randint(1000, 9999))
                        device_id = f"SB{timestamp}{random_num}"
                        retry_count += 1
            
            # 检查设备ID是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE device_id = %s", (device_id,))
            existing_device = cursor.fetchone()
            if existing_device:
                return jsonify({
                    'success': False,
                    'message': f"设备ID {device_id} 已存在"
                }), 400
            
            # 插入新用户 - 简化版，只包含基本信息
            sql = """
            INSERT INTO smart_band_users (
                id, username, nickname, age, device_id, register_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                new_id, 
                data['username'], 
                data['nickname'], 
                data['age'], 
                device_id,
                data['registerTime']
            ))
            
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f"成功创建用户 {data['username']}",
                'data': {
                    'id': new_id,
                    'username': data['username']
                }
            })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"创建用户错误: {str(e)}")
        print(f"错误详情: {error_trace}")
        return jsonify({
            'success': False,
            'message': f'创建用户失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/register.html')
def register_page():
    """提供注册页面"""
    return send_file('register.html')

@app.route('/test_api.html')
def test_api_page():
    """提供API测试页面"""
    return send_file('test_api.html')

@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_admin_profile():
    """获取当前管理员信息"""
    try:
        # 从请求头获取用户名（实际应该从token解析）
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': '未授权'
            }), 401
        
        # 从请求参数获取用户名（简单处理）
        username = request.args.get('username', '')
        
        if not username:
            return jsonify({
                'success': False,
                'message': '用户名不能为空'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, nickname, role, status, last_login, avatar FROM admins WHERE username = %s",
                (username,)
            )
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 404
            
            # 格式化管理员数据
            admin_data = {
                'id': admin['id'],
                'username': admin['username'],
                'nickname': admin['nickname'],
                'role': admin['role'],
                'status': admin['status'],
                'lastLogin': admin['last_login'].strftime('%Y-%m-%d %H:%M:%S') if admin['last_login'] else '从未登录',
                'avatar': admin['avatar']
            }
            
            return jsonify({
                'success': True,
                'data': admin_data
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取管理员信息失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_admin_profile():
    """更新当前管理员信息"""
    try:
        # 从请求头获取用户名（实际应该从token解析）
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': '未授权'
            }), 401
        
        data = request.json
        username = data.get('username', '')
        
        if not username:
            return jsonify({
                'success': False,
                'message': '用户名不能为空'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 查询管理员
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '管理员不存在'
                }), 404
            
            admin_id = admin['id']
            
            # 准备更新的字段
            update_fields = {}
            
            # 处理头像更新
            if 'avatar' in data and data['avatar'] and data['avatar'].startswith('data:image/'):
                avatar_url = save_base64_image(data['avatar'], admin_id)
                if avatar_url:
                    update_fields['avatar'] = avatar_url
            elif 'avatar' in data:
                update_fields['avatar'] = data['avatar']
            
            # 处理其他字段
            if 'nickname' in data:
                update_fields['nickname'] = data['nickname']
            
            # 如果没有任何字段需要更新，则直接返回
            if not update_fields:
                return jsonify({
                    'success': True,
                    'message': '无需更新',
                    'data': {
                        'id': admin_id,
                        'username': admin['username'],
                        'nickname': admin['nickname'],
                        'avatar': admin['avatar']
                    }
                })
            
            # 构建更新SQL
            sql_parts = []
            values = []
            
            for field, value in update_fields.items():
                sql_parts.append(f"{field} = %s")
                values.append(value)
            
            # 添加WHERE条件参数
            values.append(admin_id)
            
            # 执行更新
            sql = f"UPDATE admins SET {', '.join(sql_parts)} WHERE id = %s"
            cursor.execute(sql, values)
            connection.commit()
            
            # 查询更新后的数据
            cursor.execute(
                "SELECT id, username, nickname, avatar FROM admins WHERE id = %s",
                (admin_id,)
            )
            updated_admin = cursor.fetchone()
            
            return jsonify({
                'success': True,
                'message': '更新成功',
                'data': {
                    'id': updated_admin['id'],
                    'username': updated_admin['username'],
                    'nickname': updated_admin['nickname'],
                    'avatar': updated_admin['avatar']
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins/<int:admin_id>/avatar', methods=['POST'])
@token_required
def update_admin_avatar(admin_id):
    """更新管理员头像"""
    try:
        # 从请求头验证授权（简化处理）
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': '未授权'
            }), 401
        
        if 'avatar' not in request.json or not request.json['avatar']:
            return jsonify({
                'success': False,
                'message': '头像数据不能为空'
            }), 400
        
        avatar_data = request.json['avatar']
        
        # 验证管理员是否存在
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM admins WHERE id = %s", (admin_id,))
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '管理员不存在'
                }), 404
            
            # 保存头像
            avatar_url = save_base64_image(avatar_data, admin_id)
            
            if not avatar_url:
                return jsonify({
                    'success': False,
                    'message': '头像保存失败'
                }), 500
            
            # 更新数据库
            cursor.execute(
                "UPDATE admins SET avatar = %s WHERE id = %s",
                (avatar_url, admin_id)
            )
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': '头像更新成功',
                'data': {
                    'avatar': avatar_url
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新头像失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/admins/<int:admin_id>', methods=['PUT'])
@token_required
def update_admin(admin_id):
    """更新管理员信息"""
    try:
        # 从请求头验证授权（简化处理）
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': '未授权'
            }), 401
        
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': '无效的数据'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 检查管理员是否存在
            cursor.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
            admin = cursor.fetchone()
            
            if not admin:
                return jsonify({
                    'success': False,
                    'message': '管理员不存在'
                }), 404
            
            # 准备更新的字段
            update_fields = {}
            
            # 处理头像上传
            if 'avatar' in data and data['avatar'] and data['avatar'].startswith('data:image/'):
                print(f"处理头像数据，长度: {len(data['avatar'])}")
                avatar_url = save_base64_image(data['avatar'], admin_id)
                if avatar_url:
                    update_fields['avatar'] = avatar_url
                    print(f"保存头像成功: {avatar_url}")
                else:
                    print("保存头像失败")
            
            # 处理其他字段
            for field in ['nickname', 'role', 'status']:
                if field in data:
                    update_fields[field] = data[field]
            
            # 如果提供了密码，更新密码
            if 'password' in data and data['password']:
                update_fields['password_hash'] = generate_password_hash(data['password'])
            
            # 如果没有任何字段需要更新，则直接返回
            if not update_fields:
                return jsonify({
                    'success': False,
                    'message': '没有提供需要更新的数据'
                }), 400
            
            # 构建更新SQL
            set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
            values = list(update_fields.values())
            values.append(admin_id)  # WHERE条件的参数
            
            # 执行更新
            sql = f"UPDATE admins SET {set_clause} WHERE id = %s"
            print(f"执行SQL: {sql}, 参数: {values}")
            cursor.execute(sql, values)
            connection.commit()
            
            # 查询更新后的管理员信息
            cursor.execute("SELECT id, username, nickname, role, avatar FROM admins WHERE id = %s", (admin_id,))
            updated_admin = cursor.fetchone()
            
            return jsonify({
                'success': True,
                'message': '管理员更新成功',
                'data': {
                    'id': updated_admin['id'],
                    'username': updated_admin['username'],
                    'nickname': updated_admin['nickname'],
                    'role': updated_admin['role'],
                    'avatar': updated_admin['avatar']
                }
            })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"更新管理员失败: {str(e)}")
        print(f"错误详情: {error_details}")
        return jsonify({
            'success': False,
            'message': f'更新管理员失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

# 静态文件服务（用于访问头像）
@app.route('/static/<path:path>')
def serve_static(path):
    """服务所有静态文件"""
    return send_from_directory(STATIC_FOLDER, path)

# 添加智能手环用户接口
@app.route('/api/smart-band-users/', methods=['GET'])
@token_required
def get_smart_band_users():
    """获取所有智能手环用户"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM smart_band_users")
            users = cursor.fetchall()
            
            # 将数据转换为前端需要的格式
            formatted_users = []
            for user in users:
                formatted_users.append({
                    'id': user['id'],
                    'username': user['username'],
                    'nickname': user['nickname'],
                    'age': user['age'],
                    'deviceId': user['device_id'],
                    'registerTime': user['register_time'].strftime('%Y-%m-%d') if user['register_time'] else None
                })
            
            return jsonify({
                'success': True,
                'data': formatted_users
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取智能手环用户数据失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/smart-band-users/<int:user_id>', methods=['GET'])
@token_required
def get_smart_band_user(user_id):
    """获取单个智能手环用户"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM smart_band_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 404
            
            # 将数据转换为前端需要的格式
            formatted_user = {
                'id': user['id'],
                'username': user['username'],
                'nickname': user['nickname'],
                'age': user['age'],
                'deviceId': user['device_id'],
                'registerTime': user['register_time'].strftime('%Y-%m-%d') if user['register_time'] else None
            }
            
            return jsonify({
                'success': True,
                'data': formatted_user
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取智能手环用户数据失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/smart-band-users/', methods=['POST'])
@token_required
def create_smart_band_user():
    """创建新智能手环用户"""
    try:
        data = request.json
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE username = %s", (data['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': f"用户 {data['username']} 已存在"
                }), 400
                
            # 获取当前最大ID
            cursor.execute("SELECT MAX(id) as max_id FROM smart_band_users")
            result = cursor.fetchone()
            new_id = 1
            if result['max_id']:
                new_id = result['max_id'] + 1
            
            # 如果没有提供设备ID或为空，生成一个唯一的设备ID
            device_id = data.get('deviceId', '')
            if not device_id:
                # 生成随机设备ID
                import random
                timestamp = str(int(time.time()))[-4:]
                random_num = str(random.randint(1000, 9999))
                device_id = f"SB{timestamp}{random_num}"
                
                # 确保生成的设备ID唯一
                is_unique = False
                retry_count = 0
                while not is_unique and retry_count < 10:
                    cursor.execute("SELECT id FROM smart_band_users WHERE device_id = %s", (device_id,))
                    if not cursor.fetchone():
                        is_unique = True
                    else:
                        random_num = str(random.randint(1000, 9999))
                        device_id = f"SB{timestamp}{random_num}"
                        retry_count += 1
            
            # 检查设备ID是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE device_id = %s", (device_id,))
            existing_device = cursor.fetchone()
            if existing_device:
                return jsonify({
                    'success': False,
                    'message': f"设备ID {device_id} 已存在"
                }), 400
            
            # 插入新用户
            sql = """
            INSERT INTO smart_band_users (
                id, username, nickname, age, device_id, register_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
            """
            current_time = datetime.datetime.now()
            cursor.execute(sql, (
                new_id, 
                data['username'], 
                data.get('nickname', data['username']), 
                data.get('age', 0), 
                device_id,
                current_time
            ))
            
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f"成功创建用户 {data['username']}",
                'data': {
                    'id': new_id,
                    'username': data['username'],
                    'deviceId': device_id
                }
            })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"创建智能手环用户错误: {str(e)}")
        print(f"错误详情: {error_trace}")
        return jsonify({
            'success': False,
            'message': f'创建智能手环用户失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 