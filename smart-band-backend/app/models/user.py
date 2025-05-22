from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 以下字段将在导入默认数据时通过从字典创建的对象临时存在，但不会写入数据库
    # 因为这些字段在实际的数据库表中不存在
    def to_dict(self):
        """将用户数据转换为字典格式，方便API返回"""
        return {
            'id': self.id,
            'username': self.username,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """从字典数据创建用户对象"""
        user = User(
            username=data.get('username'),
            age=data.get('age'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        if 'password' in data:
            user.password = data.get('password')
        else:
            # 设置默认密码
            user.password = 'password123'
        
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'