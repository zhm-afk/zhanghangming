from app.models.user import User
from app.extensions import db
from datetime import datetime

class UserService:
    @staticmethod
    def get_all_users():
        """获取所有用户"""
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_device_id(device_id):
        """根据设备ID获取用户"""
        return User.query.filter_by(device_id=device_id).first()
    
    @staticmethod
    def create_user(user_data):
        """创建新用户"""
        user = User.from_dict(user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, user_data):
        """更新用户信息"""
        user = UserService.get_user_by_id(user_id)
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
        
        # 更新健康数据
        if 'heartRate' in user_data:
            user.heart_rate = user_data['heartRate']
        
        if 'bloodPressure' in user_data:
            blood_pressure = user_data['bloodPressure']
            if 'systolic' in blood_pressure:
                user.systolic_pressure = blood_pressure['systolic']
            if 'diastolic' in blood_pressure:
                user.diastolic_pressure = blood_pressure['diastolic']
        
        if 'steps' in user_data:
            user.steps = user_data['steps']
        
        # 更新位置数据
        if 'location' in user_data:
            location = user_data['location']
            if 'lat' in location:
                user.latitude = location['lat']
            if 'lng' in location:
                user.longitude = location['lng']
            if 'area' in location:
                user.area = location['area']
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = UserService.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def import_default_users(default_users):
        """导入默认用户数据"""
        users_count = User.query.count()
        if users_count == 0:
            for user_data in default_users:
                user = User.from_dict(user_data)
                db.session.add(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_user_health_data(username):
        """获取用户健康数据"""
        user = UserService.get_user_by_username(username)
        if not user:
            return None
        
        return {
            'heartRate': user.heart_rate,
            'bloodPressure': {
                'systolic': user.systolic_pressure,
                'diastolic': user.diastolic_pressure
            },
            'steps': user.steps
        }
    
    @staticmethod
    def get_user_location(username):
        """获取用户位置数据"""
        user = UserService.get_user_by_username(username)
        if not user:
            return None
        
        return {
            'lat': user.latitude,
            'lng': user.longitude,
            'area': user.area
        }
    
    @staticmethod
    def calculate_average_heart_rate():
        """计算所有用户的平均心率"""
        result = db.session.query(db.func.avg(User.heart_rate)).scalar()
        return int(result) if result else 0
    
    @staticmethod
    def calculate_average_blood_pressure():
        """计算所有用户的平均血压"""
        avg_systolic = db.session.query(db.func.avg(User.systolic_pressure)).scalar()
        avg_diastolic = db.session.query(db.func.avg(User.diastolic_pressure)).scalar()
        
        return {
            'systolic': int(avg_systolic) if avg_systolic else 0,
            'diastolic': int(avg_diastolic) if avg_diastolic else 0
        }
    
    @staticmethod
    def calculate_average_steps():
        """计算所有用户的平均步数"""
        result = db.session.query(db.func.avg(User.steps)).scalar()
        return int(result) if result else 0
    
    @staticmethod
    def get_heart_rate_distribution():
        """获取心率分布"""
        normal_min = 60
        normal_max = 100
        
        low_count = User.query.filter(User.heart_rate < normal_min).count()
        normal_count = User.query.filter(User.heart_rate.between(normal_min, normal_max)).count()
        high_count = User.query.filter(User.heart_rate > normal_max).count()
        
        return {
            'normal': normal_count,
            'high': high_count,
            'low': low_count
        } 