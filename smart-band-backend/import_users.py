import os
import sys
from datetime import datetime
import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ailing@200930',
    'db': 'smart_band',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 默认用户数据，与前端的userData.js保持一致
default_users = [
    {
        'id': 1,
        'username': '张三',
        'nickname': '张三',
        'age': 28,
        'device_id': 'SB1001',
        'register_time': '2024-05-01',
        'heart_rate': 75,
        'systolic_pressure': 120,
        'diastolic_pressure': 80,
        'steps': 8000,
        'latitude': 39.908,
        'longitude': 116.397,
        'area': '海淀区'
    },
    {
        'id': 2,
        'username': '李四',
        'nickname': '李四',
        'age': 35,
        'device_id': 'SB1002',
        'register_time': '2024-05-03',
        'heart_rate': 82,
        'systolic_pressure': 130,
        'diastolic_pressure': 85,
        'steps': 9000,
        'latitude': 39.915,
        'longitude': 116.404,
        'area': '朝阳区'
    },
    {
        'id': 3,
        'username': '王五',
        'nickname': '王五',
        'age': 22,
        'device_id': 'SB1003',
        'register_time': '2024-05-05',
        'heart_rate': 68,
        'systolic_pressure': 110,
        'diastolic_pressure': 75,
        'steps': 7000,
        'latitude': 39.905,
        'longitude': 116.390,
        'area': '西城区'
    },
    {
        'id': 4,
        'username': '赵六',
        'nickname': '赵六',
        'age': 45,
        'device_id': 'SB1004',
        'register_time': '2024-05-07',
        'heart_rate': 88,
        'systolic_pressure': 135,
        'diastolic_pressure': 90,
        'steps': 6000,
        'latitude': 39.920,
        'longitude': 116.410,
        'area': '东城区'
    },
    {
        'id': 5,
        'username': '钱七',
        'nickname': '钱七',
        'age': 31,
        'device_id': 'SB1005',
        'register_time': '2024-05-09',
        'heart_rate': 72,
        'systolic_pressure': 125,
        'diastolic_pressure': 82,
        'steps': 8500,
        'latitude': 39.925,
        'longitude': 116.415,
        'area': '丰台区'
    }
]

def create_tables(connection):
    """创建用户表"""
    with connection.cursor() as cursor:
        # 先删除可能存在的表
        cursor.execute("DROP TABLE IF EXISTS smart_band_users;")
        
        # 创建用户表
        cursor.execute("""
        CREATE TABLE smart_band_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            nickname VARCHAR(50),
            age INT,
            device_id VARCHAR(20) UNIQUE,
            register_time DATE,
            heart_rate INT,
            systolic_pressure INT,
            diastolic_pressure INT,
            steps INT,
            latitude FLOAT,
            longitude FLOAT,
            area VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        
        connection.commit()
        print("用户表创建成功")

def import_users(connection, users):
    """导入用户数据"""
    with connection.cursor() as cursor:
        for user in users:
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE username = %s", (user['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"用户 {user['username']} 已存在，跳过")
                continue
                
            # 插入新用户
            sql = """
            INSERT INTO smart_band_users (
                id, username, nickname, age, device_id, register_time,
                heart_rate, systolic_pressure, diastolic_pressure, steps,
                latitude, longitude, area
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                user['id'], 
                user['username'], 
                user['nickname'], 
                user['age'], 
                user['device_id'], 
                user['register_time'],
                user['heart_rate'], 
                user['systolic_pressure'], 
                user['diastolic_pressure'], 
                user['steps'],
                user['latitude'], 
                user['longitude'], 
                user['area']
            ))
            
        connection.commit()
        print(f"成功导入 {len(users)} 名用户")

def view_users(connection):
    """查看所有用户数据"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM smart_band_users")
        users = cursor.fetchall()
        
        print("\n当前数据库中的用户信息:")
        print("-" * 80)
        for user in users:
            print(f"ID: {user['id']}, 用户名: {user['username']}, 昵称: {user['nickname']}, 年龄: {user['age']}, 设备ID: {user['device_id']}")
            print(f"心率: {user['heart_rate']}, 血压: {user['systolic_pressure']}/{user['diastolic_pressure']}, 步数: {user['steps']}")
            print(f"位置: {user['latitude']}, {user['longitude']} - {user['area']}")
            print("-" * 80)
        
        return users

def main():
    """主函数"""
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        print("MySQL连接成功")
        
        # 创建表
        create_tables(connection)
        
        # 导入用户数据
        import_users(connection, default_users)
        
        # 查看用户数据
        view_users(connection)
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main() 