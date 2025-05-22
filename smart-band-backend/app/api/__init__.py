from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)
devices_bp = Blueprint('devices', __name__)
health_data_bp = Blueprint('health_data', __name__)
feedback_bp = Blueprint('feedback', __name__)
ai_assistant_bp = Blueprint('ai_assistant', __name__)

# 导入路由
from app.api import auth, users, devices, health_data, feedback, ai_assistant