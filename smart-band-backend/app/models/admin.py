from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='normal')  # normal 或 super
    status = db.Column(db.String(20), default='离线')  # 在线 或 离线
    last_login = db.Column(db.DateTime)
    avatar = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """将管理员数据转换为字典格式，方便API返回"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'role': self.role,
            'status': self.status,
            'lastLogin': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else '从未登录',
            'avatar': self.avatar
        }
    
    @staticmethod
    def from_dict(data):
        """从字典数据创建管理员对象"""
        admin = Admin(
            username=data.get('username'),
            nickname=data.get('nickname'),
            role=data.get('role', 'normal'),
            status=data.get('status', '离线'),
            avatar=data.get('avatar', '')
        )
        
        # 设置密码
        if 'password' in data:
            admin.password = data['password']
        
        return admin 