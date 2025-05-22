from datetime import datetime
from app.extensions import db

class HealthData(db.Model):
    __tablename__ = 'health_data'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 健康指标
    heart_rate = db.Column(db.Integer, nullable=True)
    systolic_pressure = db.Column(db.Integer, nullable=True)  # 收缩压
    diastolic_pressure = db.Column(db.Integer, nullable=True)  # 舒张压
    steps = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Float, nullable=True)
    sleep_duration = db.Column(db.Integer, nullable=True)  # 睡眠时长（分钟）
    oxygen_saturation = db.Column(db.Float, nullable=True)  # 血氧饱和度
    temperature = db.Column(db.Float, nullable=True)  # 体温
    
    # 环境数据
    environment_temperature = db.Column(db.Float, nullable=True)  # 环境温度
    humidity = db.Column(db.Float, nullable=True)  # 湿度
    pressure = db.Column(db.Float, nullable=True)  # 气压
    
    def __repr__(self):
        return f'<HealthData {self.id} for Customer {self.customer_id}>'