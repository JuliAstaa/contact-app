from app.models.mycontact import Users
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True