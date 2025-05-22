from app.models.smart_band_user import SmartBandUser
from app.extensions import db
from datetime import datetime

class SmartBandUserService:
    @staticmethod
    def get_all_users():
        """获取所有智能手环用户"""
        return SmartBandUser.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return SmartBandUser.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户"""
        return SmartBandUser.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_device_id(device_id):
        """根据设备ID获取用户"""
        return SmartBandUser.query.filter_by(device_id=device_id).first()
    
    @staticmethod
    def create_user(user_data):
        """创建新用户"""
        user = SmartBandUser.from_dict(user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, user_data):
        """更新用户信息"""
        user = SmartBandUserService.get_user_by_id(user_id)
        if not user:
            return None
        
        # 更新基本信息
        if 'username' in user_data:
            user.username = user_data['username']
        if 'nickname' in user_data:
            user.nickname = user_data['nickname']
        if 'age' in user_data:
            user.age = user_data['age']
        if 'deviceId' in user_data:
            user.device_id = user_data['deviceId']
        if 'registerTime' in user_data:
            try:
                user.register_time = datetime.strptime(user_data['registerTime'], '%Y-%m-%d').date()
            except:
                pass
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = SmartBandUserService.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False 