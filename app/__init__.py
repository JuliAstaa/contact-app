from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()

db: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()

class App:
    def __init__(self):
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.app: Flask = Flask(__name__)
        self.config()
        self.database()
        self.jwt()
        self.router()
        CORS(self.app)

    def config(self):
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(self.abs_path, 'my_contact.db')}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    def database(self):
        db.init_app(self.app)
    
    def jwt(self):
        jwt.init_app(self.app)

    def router(self):
        from app.routes.contact_routes import ContactRoutes
        from app.routes.api_routes import ApiContactRoutes
        from app.routes.auth_routes import AuthRoutes
        contact_api = ApiContactRoutes()
        contact = ContactRoutes()
        auth = AuthRoutes()
        self.app.register_blueprint(contact.contact)
        self.app.register_blueprint(contact_api.contact_api)
        self.app.register_blueprint(auth.auth)
        

    def app(self):
        return self.app.run()





