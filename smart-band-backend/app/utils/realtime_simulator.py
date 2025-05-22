import time
import threading
from datetime import datetime
import random
from app.extensions import socketio
from app.models.device import Device
from app.models.health_data import HealthData
from app.utils.data_generator import simulate_real_time_health_data, simulate_device_status
from app.extensions import db

class RealtimeSimulator:
    """
    模拟实时数据生成器，用于通过WebSocket发送模拟的健康数据和设备状态更新
    """
    
    def __init__(self, data_interval=5, status_interval=10):
        """
        初始化模拟器
        
        Args:
            data_interval (int): 发送健康数据的间隔（秒）
            status_interval (int): 发送设备状态更新的间隔（秒）
        """
        self.data_interval = data_interval
        self.status_interval = status_interval
        self.running = False
        self.data_thread = None
        self.status_thread = None
        self.active_devices = {}  # 保存活跃设备的信息
    
    def start(self):
        """启动数据模拟器"""
        if self.running:
            return False
        
        self.running = True
        
        # 获取活跃设备
        self._load_active_devices()
        
        # 启动数据生成线程
        self.data_thread = threading.Thread(target=self._health_data_generator)
        self.data_thread.daemon = True
        self.data_thread.start()
        
        # 启动状态更新线程
        self.status_thread = threading.Thread(target=self._device_status_generator)
        self.status_thread.daemon = True
        self.status_thread.start()
        
        print(f"实时数据模拟器已启动，当前有 {len(self.active_devices)} 个活跃设备")
        return True
    
    def stop(self):
        """停止数据模拟器"""
        self.running = False
        if self.data_thread:
            self.data_thread.join(timeout=1.0)
        if self.status_thread:
            self.status_thread.join(timeout=1.0)
        print("实时数据模拟器已停止")
        return True
    
    def _load_active_devices(self):
        """加载活跃设备列表"""
        devices = Device.query.filter_by(status='active').all()
        
        for device in devices:
            self.active_devices[device.id] = {
                'device_id': device.id,
                'customer_id': device.customer_id,
                'device_string_id': device.device_id,
                'last_latitude': device.latitude,
                'last_longitude': device.longitude,
                'room': f'device_{device.id}'  # 为每个设备创建单独的房间
            }
    
    def _health_data_generator(self):
        """健康数据生成器线程"""
        print("健康数据生成器线程已启动")
        
        while self.running:
            # 为每个活跃设备生成并发送数据
            for device_id, device_info in self.active_devices.items():
                try:
                    # 生成模拟数据
                    data = simulate_real_time_health_data(
                        device_info['device_string_id'], 
                        device_info['customer_id']
                    )
                    
                    # 发送到对应的设备房间
                    socketio.emit('health_data_update', data, room=device_info['room'])
                    
                    # 保存到数据库
                    self._save_health_data(device_id, device_info['customer_id'], data)
                    
                except Exception as e:
                    print(f"健康数据生成错误: {str(e)}")
            
            # 等待指定间隔
            time.sleep(self.data_interval)
    
    def _device_status_generator(self):
        """设备状态生成器线程"""
        print("设备状态生成器线程已启动")
        
        while self.running:
            # 为每个活跃设备生成并发送状态更新
            devices_to_remove = []
            
            for device_id, device_info in self.active_devices.items():
                try:
                    # 生成模拟状态
                    status_data = simulate_device_status(
                        device_info['device_string_id'], 
                        device_info['customer_id']
                    )
                    
                    # 计算新的位置
                    new_latitude = device_info['last_latitude'] + status_data['latitude_change']
                    new_longitude = device_info['last_longitude'] + status_data['longitude_change']
                    
                    # 更新设备信息
                    status_data['latitude'] = new_latitude
                    status_data['longitude'] = new_longitude
                    
                    # 更新本地缓存
                    self.active_devices[device_id]['last_latitude'] = new_latitude
                    self.active_devices[device_id]['last_longitude'] = new_longitude
                    
                    # 发送到对应的设备房间
                    socketio.emit('device_status_update', status_data, room=device_info['room'])
                    
                    # 更新数据库中的设备信息
                    self._update_device_status(device_id, status_data)
                    
                    # 如果设备状态变为非活跃，标记为需要移除
                    if status_data['status'] != 'active':
                        devices_to_remove.append(device_id)
                    
                except Exception as e:
                    print(f"设备状态更新错误: {str(e)}")
            
            # 移除非活跃设备
            for device_id in devices_to_remove:
                del self.active_devices[device_id]
                print(f"设备 {device_id} 已变为非活跃状态，从模拟器移除")
            
            # 等待指定间隔
            time.sleep(self.status_interval)
    
    def _save_health_data(self, device_id, customer_id, data):
        """保存健康数据到数据库"""
        try:
            timestamp = datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp']
            
            health_data = HealthData(
                customer_id=customer_id,
                device_id=device_id,
                timestamp=timestamp,
                heart_rate=data['heart_rate'],
                systolic_pressure=data['systolic_pressure'],
                diastolic_pressure=data['diastolic_pressure'],
                steps=data['steps'],
                calories=data['calories'],
                sleep_duration=data['sleep_duration'],
                oxygen_saturation=data['oxygen_saturation'],
                temperature=data['temperature'],
                environment_temperature=data['environment_temperature'],
                humidity=data['humidity'],
                pressure=data['pressure']
            )
            
            db.session.add(health_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"保存健康数据错误: {str(e)}")
    
    def _update_device_status(self, device_id, data):
        """更新设备状态到数据库"""
        try:
            device = Device.query.get(device_id)
            if device:
                device.status = data['status']
                device.battery_level = data['battery_level']
                device.latitude = data['latitude']
                device.longitude = data['longitude']
                device.last_sync = datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp']
                device.location_updated_at = device.last_sync
                
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"更新设备状态错误: {str(e)}")
    
    def register_device_to_room(self, device_id, sid):
        """
        将WebSocket客户端注册到设备房间
        
        Args:
            device_id: 设备ID
            sid: Socket会话ID
        """
        room_name = f'device_{device_id}'
        socketio.server.enter_room(sid, room_name)
        print(f"客户端 {sid} 已加入设备 {device_id} 的房间")
        return True
    
    def get_active_device_count(self):
        """获取当前活跃设备数量"""
        return len(self.active_devices)


# 创建全局实例
simulator = RealtimeSimulator()

# SocketIO 事件处理
@socketio.on('connect')
def handle_connect():
    print(f"客户端已连接: {socketio.sid}")
    return True

@socketio.on('disconnect')
def handle_disconnect():
    print(f"客户端已断开连接: {socketio.sid}")
    return True

@socketio.on('subscribe_device')
def handle_subscribe_device(data):
    """
    订阅设备数据更新
    
    Args:
        data: 包含device_id字段的字典
    """
    device_id = data.get('device_id')
    if not device_id:
        return {'success': False, 'message': '缺少设备ID'}
    
    # 查找设备
    device = Device.query.get(device_id)
    if not device:
        return {'success': False, 'message': '设备不存在'}
    
    # 注册到设备房间
    simulator.register_device_to_room(device_id, socketio.sid)
    
    return {'success': True, 'message': f'已订阅设备 {device_id} 的数据更新'}

# 启动模拟器的函数
def start_simulator():
    """启动实时数据模拟器"""
    return simulator.start()

# 停止模拟器的函数
def stop_simulator():
    """停止实时数据模拟器"""
    return simulator.stop() 