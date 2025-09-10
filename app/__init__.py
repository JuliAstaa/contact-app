from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

db: SQLAlchemy = SQLAlchemy()

class App:
    def __init__(self):
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.app: Flask = Flask(__name__)
        self.config()
        self.database()
        self.router()

    def config(self):
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(self.abs_path, 'my_contact.db')}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    def database(self):
        db.init_app(self.app)

    def router(self):
        from app.routes.contact_routes import ContactRoutes
        contact = ContactRoutes()
        self.app.register_blueprint(contact.contact)
        

    def app(self):
        return self.app.run()





