from datetime import datetime
from app.extensions import db

class SmartBandUser(db.Model):
    __tablename__ = 'smart_band_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    device_id = db.Column(db.String(20), unique=True)
    register_time = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """将用户数据转换为字典格式，方便API返回"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'age': self.age,
            'deviceId': self.device_id,
            'registerTime': self.register_time.strftime('%Y-%m-%d') if self.register_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """从字典数据创建用户对象"""
        user = SmartBandUser(
            username=data.get('username'),
            nickname=data.get('nickname'),
            age=data.get('age'),
            device_id=data.get('deviceId')
        )
        
        if 'registerTime' in data:
            try:
                user.register_time = datetime.strptime(data.get('registerTime'), '%Y-%m-%d').date()
            except:
                pass
        
        return user
        
    def __repr__(self):
        return f'<SmartBandUser {self.username}>' 