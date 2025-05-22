from datetime import datetime
from app.extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    devices = db.relationship('Device', backref='customer', lazy='dynamic')
    health_data = db.relationship('HealthData', backref='customer', lazy='dynamic')
    
    def __repr__(self):
        return f'<Customer {self.username}>'