from app.models.mycontact import MyContact
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class MyContactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MyContact
        load_instance = True