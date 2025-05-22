import random
import string
from datetime import datetime, timedelta
import math

# Customer data generation
def generate_customer_data(count=50):
    """Generate random customer data"""
    customers = []
    genders = ['男', '女']
    
    for i in range(1, count + 1):
        username = f'user{i:03d}'
        nickname = f'用户{i:03d}'
        age = random.randint(18, 80)
        gender = random.choice(genders)
        phone = f'1{random.choice(["3", "5", "7", "8", "9"])}{random.randint(100000000, 999999999)}'
        email = f'{username}@example.com'
        
        customers.append({
            'username': username,
            'nickname': nickname,
            'age': age,
            'gender': gender,
            'phone': phone,
            'email': email,
        })
    
    return customers

# Device data generation
def generate_device_data(customer_ids, count=100):
    """Generate random device data"""
    devices = []
    statuses = ['active', 'inactive', 'maintenance']
    
    for i in range(1, count + 1):
        device_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        device_name = f'Smart Band {i:03d}'
        customer_id = random.choice(customer_ids)
        status = random.choices(statuses, weights=[0.8, 0.15, 0.05])[0]
        battery_level = random.randint(10, 100)
        firmware = f'1.{random.randint(0, 9)}.{random.randint(0, 9)}'
        last_sync = datetime.utcnow() - timedelta(hours=random.randint(0, 48))
        
        # 位置信息 (中国大致范围)
        latitude = random.uniform(22.0, 45.0)  # 中国纬度范围
        longitude = random.uniform(100.0, 130.0)  # 中国经度范围
        area = random.choice(['北京', '上海', '广州', '深圳', '成都', '重庆', '杭州', '南京', '武汉', '西安'])
        location_updated_at = datetime.utcnow() - timedelta(minutes=random.randint(0, 300))
        
        devices.append({
            'device_id': device_id,
            'device_name': device_name,
            'customer_id': customer_id,
            'status': status,
            'battery_level': battery_level,
            'firmware': firmware,
            'last_sync': last_sync,
            'latitude': latitude,
            'longitude': longitude,
            'area': area,
            'location_updated_at': location_updated_at
        })
    
    return devices

# Health data generation
def generate_health_data(customer_device_pairs, days=7, readings_per_day=24):
    """Generate random health data for the given customer-device pairs over a period of days"""
    health_data = []
    
    for customer_id, device_id in customer_device_pairs:
        # Generate data for each day
        for day in range(days):
            # Generate data for each reading in a day
            for hour in range(readings_per_day):
                # Basic timestamp for this reading
                timestamp = datetime.utcnow() - timedelta(days=day, hours=hour)
                
                # Health metrics with some randomness but also some patterns
                hour_of_day = hour % 24
                
                # Heart rate varies by time of day
                base_heart_rate = 70
                if 0 <= hour_of_day < 6:  # Sleep
                    heart_rate = random.randint(55, 65)
                elif 6 <= hour_of_day < 9:  # Morning activity
                    heart_rate = random.randint(70, 85)
                elif 9 <= hour_of_day < 12:  # Morning work
                    heart_rate = random.randint(65, 75)
                elif 12 <= hour_of_day < 14:  # Lunch
                    heart_rate = random.randint(70, 80)
                elif 14 <= hour_of_day < 18:  # Afternoon work
                    heart_rate = random.randint(65, 75)
                elif 18 <= hour_of_day < 21:  # Evening activity
                    heart_rate = random.randint(75, 90)
                else:  # Evening rest
                    heart_rate = random.randint(60, 70)
                
                # Blood pressure
                systolic = random.randint(110, 130)
                diastolic = random.randint(70, 85)
                
                # Steps - more during active hours
                base_steps = 0
                if 6 <= hour_of_day < 9:
                    base_steps = random.randint(1000, 2000)
                elif 12 <= hour_of_day < 14:
                    base_steps = random.randint(500, 1000)
                elif 17 <= hour_of_day < 20:
                    base_steps = random.randint(1500, 3000)
                else:
                    base_steps = random.randint(100, 500)
                
                # Calories
                calories = base_steps * 0.05 + random.uniform(0, 50)
                
                # Sleep duration (only if night time)
                sleep_duration = None
                if 0 <= hour_of_day < 8:
                    sleep_duration = random.randint(20, 60)  # minutes per hour
                
                # Blood oxygen
                oxygen_saturation = random.uniform(94, 99)
                
                # Body temperature
                temperature = random.uniform(36.3, 37.2)
                
                # Environment data
                environment_temperature = random.uniform(15, 30)
                humidity = random.uniform(30, 70)
                pressure = random.uniform(990, 1030)
                
                health_data.append({
                    'customer_id': customer_id,
                    'device_id': device_id,
                    'timestamp': timestamp,
                    'heart_rate': heart_rate,
                    'systolic_pressure': systolic,
                    'diastolic_pressure': diastolic,
                    'steps': base_steps,
                    'calories': calories,
                    'sleep_duration': sleep_duration,
                    'oxygen_saturation': oxygen_saturation,
                    'temperature': temperature,
                    'environment_temperature': environment_temperature,
                    'humidity': humidity,
                    'pressure': pressure
                })
    
    return health_data

# Feedback data generation
def generate_feedback_data(customer_ids, count=20):
    """Generate random feedback data"""
    feedback_types = ['bug', 'feature', 'improvement', 'question']
    statuses = ['pending', 'in_progress', 'resolved', 'closed']
    feedback_data = []
    
    subjects = [
        "手环连接问题", "电池续航问题", "计步不准确", "心率监测异常",
        "睡眠监测建议", "新功能建议", "界面优化建议", "数据同步问题",
        "手环佩戴不舒适", "防水性能问题", "健康提醒功能建议", "运动模式建议"
    ]
    
    contents = [
        "我的手环经常断开连接，需要重新配对",
        "电池只能用一天，宣传是可以用三天",
        "计步功能不准确，实际步数和手环显示相差很大",
        "心率监测时常出现数据异常，忽高忽低",
        "希望能够改进睡眠监测算法，现在的深浅睡眠判断不准",
        "建议增加月经周期监测功能",
        "希望能够自定义界面颜色和布局",
        "数据同步到APP经常失败，需要多次尝试",
        "长时间佩戴手环会感到不舒适，希望改进材质",
        "按说明书可以游泳使用，但实际用了几次后就进水了",
        "希望增加久坐提醒和喝水提醒功能",
        "建议增加更多专业的运动模式，比如瑜伽、高尔夫等"
    ]
    
    for i in range(count):
        customer_id = random.choice(customer_ids)
        feedback_type = random.choice(feedback_types)
        status = random.choice(statuses)
        subject = random.choice(subjects)
        content = random.choice(contents)
        created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        
        feedback_data.append({
            'customer_id': customer_id,
            'type': feedback_type,
            'status': status,
            'subject': subject,
            'content': content,
            'created_at': created_at
        })
    
    return feedback_data

# Real-time data simulation for WebSocket
def simulate_real_time_health_data(device_id, customer_id):
    """Simulate real-time health data for a specific device"""
    timestamp = datetime.utcnow()
    
    # Get the hour to simulate daily patterns
    hour = timestamp.hour
    
    # Heart rate varies by time of day
    if 0 <= hour < 6:  # Sleep
        heart_rate = random.randint(55, 65)
    elif 6 <= hour < 9:  # Morning activity
        heart_rate = random.randint(70, 85)
    elif 9 <= hour < 12:  # Morning work
        heart_rate = random.randint(65, 75)
    elif 12 <= hour < 14:  # Lunch
        heart_rate = random.randint(70, 80)
    elif 14 <= hour < 18:  # Afternoon work
        heart_rate = random.randint(65, 75)
    elif 18 <= hour < 21:  # Evening activity
        heart_rate = random.randint(75, 90)
    else:  # Evening rest
        heart_rate = random.randint(60, 70)
    
    # Add some randomness to heart_rate
    heart_rate = max(40, min(180, heart_rate + random.randint(-5, 5)))
    
    # Blood pressure
    systolic = random.randint(110, 130)
    diastolic = random.randint(70, 85)
    
    # Steps - accumulate throughout the day
    steps_per_reading = 0
    if 6 <= hour < 22:  # Awake hours
        steps_per_reading = random.randint(50, 500)
    
    # Calories
    calories = steps_per_reading * 0.05 + random.uniform(0, 10)
    
    # Sleep minutes in this period
    sleep_duration = None
    if 0 <= hour < 8:
        sleep_duration = random.randint(20, 60)  # minutes per reading
    
    # Blood oxygen
    oxygen_saturation = round(random.uniform(94, 99), 1)
    
    # Body temperature
    temperature = round(random.uniform(36.3, 37.2), 1)
    
    # Environment data
    environment_temperature = round(random.uniform(15, 30), 1)
    humidity = round(random.uniform(30, 70), 1)
    pressure = round(random.uniform(990, 1030), 1)
    
    return {
        'device_id': device_id,
        'customer_id': customer_id,
        'timestamp': timestamp.isoformat(),
        'heart_rate': heart_rate,
        'systolic_pressure': systolic,
        'diastolic_pressure': diastolic,
        'steps': steps_per_reading,
        'calories': round(calories, 2),
        'sleep_duration': sleep_duration,
        'oxygen_saturation': oxygen_saturation,
        'temperature': temperature,
        'environment_temperature': environment_temperature,
        'humidity': humidity,
        'pressure': pressure
    }

# Device status simulation for WebSocket
def simulate_device_status(device_id, customer_id):
    """Simulate device status updates"""
    timestamp = datetime.utcnow()
    
    battery_level = random.randint(10, 100)
    status = random.choices(['active', 'inactive', 'maintenance'], weights=[0.9, 0.08, 0.02])[0]
    
    # Simulate movement (small changes in location)
    latitude_change = random.uniform(-0.001, 0.001)
    longitude_change = random.uniform(-0.001, 0.001)
    
    return {
        'device_id': device_id,
        'customer_id': customer_id,
        'timestamp': timestamp.isoformat(),
        'battery_level': battery_level,
        'status': status,
        'latitude_change': latitude_change,
        'longitude_change': longitude_change
    } 