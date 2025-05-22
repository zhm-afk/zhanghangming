import pymysql
from datetime import datetime

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ailing@200930',
    'db': 'smart_band',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def add_user(user_data):
    """添加新用户到数据库"""
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        print("MySQL连接成功")
        
        with connection.cursor() as cursor:
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM smart_band_users WHERE username = %s", (user_data['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"用户 {user_data['username']} 已存在，无法添加")
                return False
                
            # 获取当前最大ID
            cursor.execute("SELECT MAX(id) as max_id FROM smart_band_users")
            result = cursor.fetchone()
            new_id = 1
            if result['max_id']:
                new_id = result['max_id'] + 1
            
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
                new_id, 
                user_data['username'], 
                user_data['nickname'], 
                user_data['age'], 
                f"SB{1000 + new_id}",  # 自动生成设备ID
                datetime.now().strftime('%Y-%m-%d'), # 今天的日期作为注册时间
                user_data['heart_rate'], 
                user_data['systolic_pressure'], 
                user_data['diastolic_pressure'], 
                user_data['steps'],
                user_data['latitude'], 
                user_data['longitude'], 
                user_data['area']
            ))
            
            connection.commit()
            print(f"成功添加用户 {user_data['username']}")
            
            # 查询并显示新添加的用户
            cursor.execute("SELECT * FROM smart_band_users WHERE id = %s", (new_id,))
            new_user = cursor.fetchone()
            print("\n新添加的用户信息:")
            print("-" * 80)
            print(f"ID: {new_user['id']}, 用户名: {new_user['username']}, 昵称: {new_user['nickname']}, 年龄: {new_user['age']}, 设备ID: {new_user['device_id']}")
            print(f"心率: {new_user['heart_rate']}, 血压: {new_user['systolic_pressure']}/{new_user['diastolic_pressure']}, 步数: {new_user['steps']}")
            print(f"位置: {new_user['latitude']}, {new_user['longitude']} - {new_user['area']}")
            print("-" * 80)
            
            return True
            
    except Exception as e:
        print(f"错误: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    # 用户信息输入
    print("请输入新用户信息:")
    username = input("用户名: ")
    nickname = input("昵称 (可留空使用用户名): ") or username
    
    # 数字信息验证
    while True:
        try:
            age = int(input("年龄: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            heart_rate = int(input("心率: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            systolic_pressure = int(input("收缩压: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            diastolic_pressure = int(input("舒张压: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            steps = int(input("步数: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            latitude = float(input("纬度 (例如: 39.908): "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            longitude = float(input("经度 (例如: 116.397): "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    area = input("所在区域 (例如: 海淀区): ")
    
    # 构建用户数据
    user_data = {
        'username': username,
        'nickname': nickname,
        'age': age,
        'heart_rate': heart_rate,
        'systolic_pressure': systolic_pressure,
        'diastolic_pressure': diastolic_pressure,
        'steps': steps,
        'latitude': latitude,
        'longitude': longitude,
        'area': area
    }
    
    # 添加用户
    add_user(user_data) 