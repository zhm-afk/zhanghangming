# 智能手环后端管理系统

这是一个用于管理智能手环设备和客户数据的后端系统。系统提供了设备管理、健康数据分析、用户反馈处理等功能。

## 数据模拟器

本系统提供了数据模拟器，用于生成测试数据和模拟实时数据流。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 初始化数据库

在第一次运行应用之前，需要初始化数据库并填充模拟数据：

```bash
# 创建数据库表
flask db upgrade

# 填充模拟数据
flask seed-db

# 可以自定义数据量
flask seed-db --customers 100 --devices 200 --days 14 --feedback 50
```

### 启动实时数据模拟器

实时数据模拟器通过WebSocket发送模拟的健康数据和设备状态更新：

```bash
# 启动模拟器
flask start-simulator

# 停止模拟器
flask stop-simulator
```

### 启动应用

```bash
# 开发环境
python run.py

# 或者使用gunicorn
gunicorn -k eventlet -w 1 "app:create_app()" --bind 0.0.0.0:5000
```

## API端点

系统提供以下API端点：

### 设备管理

- `GET /api/devices/` - 获取所有设备列表
- `GET /api/devices/{device_id}` - 获取设备详情
- `GET /api/devices/{device_id}/health-data` - 获取设备健康数据

### 健康数据

- `GET /api/health-data/` - 获取健康数据列表
- `GET /api/health-data/customer/{customer_id}/summary` - 获取客户健康数据概要
- `GET /api/health-data/statistics` - 获取健康数据统计信息

### 模拟器控制

- `GET /api/devices/simulator/status` - 获取模拟器状态
- `POST /api/devices/simulator/start` - 启动模拟器
- `POST /api/devices/simulator/stop` - 停止模拟器

## WebSocket 事件

模拟器通过WebSocket发送实时数据：

- `health_data_update` - 健康数据更新
- `device_status_update` - 设备状态更新

客户端可以通过发送`subscribe_device`事件订阅特定设备的数据更新：

```javascript
// 订阅设备数据
socket.emit('subscribe_device', { device_id: 123 });

// 监听健康数据更新
socket.on('health_data_update', (data) => {
  console.log('健康数据更新:', data);
});

// 监听设备状态更新
socket.on('device_status_update', (data) => {
  console.log('设备状态更新:', data);
});
``` 