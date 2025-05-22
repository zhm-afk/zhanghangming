from app.services.user_service import UserService
from app.services.admin_service import AdminService

# 默认用户数据，与前端的userData.js保持一致
default_users = [
    {
        'id': 1,
        'username': '张三',
        'nickname': '张三',
        'age': 28,
        'deviceId': 'SB1001',
        'registerTime': '2024-05-01',
        'heartRate': 75,
        'bloodPressure': { 'systolic': 120, 'diastolic': 80 },
        'steps': 8000,
        'location': {
            'lat': 39.908,
            'lng': 116.397,
            'area': '海淀区'
        }
    },
    {
        'id': 2,
        'username': '李四',
        'nickname': '李四',
        'age': 35,
        'deviceId': 'SB1002',
        'registerTime': '2024-05-03',
        'heartRate': 82,
        'bloodPressure': { 'systolic': 130, 'diastolic': 85 },
        'steps': 9000,
        'location': {
            'lat': 39.915,
            'lng': 116.404,
            'area': '朝阳区'
        }
    },
    {
        'id': 3,
        'username': '王五',
        'nickname': '王五',
        'age': 22,
        'deviceId': 'SB1003',
        'registerTime': '2024-05-05',
        'heartRate': 68,
        'bloodPressure': { 'systolic': 110, 'diastolic': 75 },
        'steps': 7000,
        'location': {
            'lat': 39.905,
            'lng': 116.390,
            'area': '西城区'
        }
    },
    {
        'id': 4,
        'username': '赵六',
        'nickname': '赵六',
        'age': 45,
        'deviceId': 'SB1004',
        'registerTime': '2024-05-07',
        'heartRate': 88,
        'bloodPressure': { 'systolic': 135, 'diastolic': 90 },
        'steps': 6000,
        'location': {
            'lat': 39.920,
            'lng': 116.410,
            'area': '东城区'
        }
    },
    {
        'id': 5,
        'username': '钱七',
        'nickname': '钱七',
        'age': 31,
        'deviceId': 'SB1005',
        'registerTime': '2024-05-09',
        'heartRate': 72,
        'bloodPressure': { 'systolic': 125, 'diastolic': 82 },
        'steps': 8500,
        'location': {
            'lat': 39.925,
            'lng': 116.415,
            'area': '丰台区'
        }
    }
]

def import_default_data():
    """导入默认数据到数据库"""
    # 导入默认管理员数据
    admins_imported = AdminService.import_default_admins()
    
    return {
        'admins_imported': admins_imported
    } 