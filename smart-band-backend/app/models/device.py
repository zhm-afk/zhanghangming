from datetime import datetime
from app.extensions import db

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    device_name = db.Column(db.String(64), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, maintenance
    battery_level = db.Column(db.Integer, default=100)
    firmware = db.Column(db.String(64), default='1.0.0')
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 位置信息
    latitude = db.Column(db.Float, default=0)
    longitude = db.Column(db.Float, default=0)
    area = db.Column(db.String(64), default='')
    location_updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    health_data = db.relationship('HealthData', backref='device', lazy='dynamic')
    
    def __repr__(self):
        return f'<Device {self.device_id}>'