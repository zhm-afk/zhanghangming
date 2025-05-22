from app.extensions import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        
    id = ma.auto_field()
    username = ma.auto_field()
    nickname = ma.auto_field()
    role = ma.auto_field()
    avatar = ma.auto_field()
    created_at = ma.auto_field()