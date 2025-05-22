import threading
import time
from app.utils.realtime_simulator import start_simulator

def start_simulator_with_delay(delay=10):
    """
    延迟启动模拟器，确保应用已完全启动
    
    Args:
        delay (int): 启动延迟（秒）
    """
    def _delayed_start():
        print(f"等待 {delay} 秒后启动数据模拟器...")
        time.sleep(delay)
        success = start_simulator()
        if success:
            print("应用启动时自动启动数据模拟器成功")
        else:
            print("应用启动时自动启动数据模拟器失败")
    
    # 创建并启动线程
    thread = threading.Thread(target=_delayed_start)
    thread.daemon = True
    thread.start()
    
    return thread 