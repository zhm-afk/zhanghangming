from flask import Flask
from flask_cors import CORS

from app.extensions import db, migrate, jwt, ma, socketio
from app.config import config_by_name

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # 初始化扩展
    CORS(app, resources={r"/api/*": {"origins": ["http://182.92.87.209:3000", "http://localhost:3000", "*"], "supports_credentials": True, "allow_headers": ["Content-Type", "Authorization"]}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    
    # 注册蓝图
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.admins import admins_bp
    from app.api.smart_band_users import smart_band_users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(admins_bp, url_prefix='/api/admins')
    app.register_blueprint(smart_band_users_bp, url_prefix='/api/smart-band-users')
    
    # 其他API蓝图
    # 如有需要可以添加设备、健康数据、反馈等API
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '请求的资源不存在'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return {'success': False, 'message': '服务器内部错误'}, 500
    
    # 初始化数据
    @app.before_first_request
    def initialize_data():
        with app.app_context():
            # 创建数据库表，注意：此时表应该已经通过迁移创建好了，这里只是导入管理员数据
            # db.create_all() 
            
            # 只导入管理员数据
            from app.utils.import_data import import_default_data
            result = import_default_data()
            app.logger.info(f"数据导入结果: {result}")
    
    # 注册CLI命令
    from app.utils.cli import register_cli_commands
    register_cli_commands(app)
    
    return app