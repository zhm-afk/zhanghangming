from app.models.admin import Admin
from app.extensions import db
from datetime import datetime

class AdminService:
    @staticmethod
    def get_all_admins():
        """获取所有管理员"""
        return Admin.query.all()
    
    @staticmethod
    def get_admin_by_id(admin_id):
        """根据ID获取管理员"""
        return Admin.query.get(admin_id)
    
    @staticmethod
    def get_admin_by_username(username):
        """根据用户名获取管理员"""
        return Admin.query.filter_by(username=username).first()
    
    @staticmethod
    def create_admin(admin_data):
        """创建新管理员"""
        admin = Admin.from_dict(admin_data)
        db.session.add(admin)
        db.session.commit()
        return admin
    
    @staticmethod
    def update_admin(admin_id, admin_data):
        """更新管理员信息"""
        admin = AdminService.get_admin_by_id(admin_id)
        if not admin:
            return None
        
        # 更新基本信息
        if 'username' in admin_data:
            admin.username = admin_data['username']
        if 'nickname' in admin_data:
            admin.nickname = admin_data['nickname']
        if 'role' in admin_data:
            admin.role = admin_data['role']
        if 'avatar' in admin_data:
            admin.avatar = admin_data['avatar']
        if 'status' in admin_data:
            admin.status = admin_data['status']
        
        # 如果有密码则更新密码
        if 'password' in admin_data and admin_data['password']:
            admin.password = admin_data['password']
        
        db.session.commit()
        return admin
    
    @staticmethod
    def delete_admin(admin_id):
        """删除管理员"""
        admin = AdminService.get_admin_by_id(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def verify_admin(username, password):
        """验证管理员登录"""
        admin = AdminService.get_admin_by_username(username)
        if admin and admin.verify_password(password):
            # 更新登录状态
            admin.status = '在线'
            admin.last_login = datetime.now()
            db.session.commit()
            return admin
        return None
    
    @staticmethod
    def logout_admin(username):
        """管理员登出"""
        admin = AdminService.get_admin_by_username(username)
        if admin:
            admin.status = '离线'
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def import_default_admins():
        """导入默认管理员数据"""
        admin_count = Admin.query.count()
        if admin_count == 0:
            default_admins = [
                {
                    'username': '张航铭',
                    'nickname': '张航铭',
                    'password': 'zhanghangming',
                    'role': 'super',
                    'status': '离线'
                },
                {
                    'username': '唐涛',
                    'nickname': '唐涛',
                    'password': 'tangtao',
                    'role': 'normal',
                    'status': '离线'
                },
                {
                    'username': '蓝金桥',
                    'nickname': '蓝金桥',
                    'password': 'lanjinqiao',
                    'role': 'normal',
                    'status': '离线'
                },
                {
                    'username': '肖欣芮',
                    'nickname': '肖欣芮',
                    'password': 'xiaoxinrui',
                    'role': 'normal',
                    'status': '离线'
                }
            ]
            
            for admin_data in default_admins:
                admin = Admin.from_dict(admin_data)
                db.session.add(admin)
            
            db.session.commit()
            return True
        
        return False 