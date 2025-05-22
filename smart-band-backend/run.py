from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == '__main__':
    # 在这里初始化socketio并运行
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)