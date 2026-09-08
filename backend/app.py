from flask import Flask
from config import LocalConfig, ProductionConfig
from database.database import db
from database.models import Admin
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from services.mail import mail
from routes import register_route
from services.cache import cache
import os



jwt = JWTManager()

app = None 

def create_app():
    app = Flask(__name__)

    app.config.from_object(LocalConfig)

    CORS(app, resources=app.config.get('CORS_RESOURCES', {r"/*": {"origins": "*"}}))
    
    jwt.init_app(app) 
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    register_route(app)
    return app

def setup_database():
    if not os.path.exists("instance/campushire.db"): 
        db.create_all() 
        admin = Admin(id = 1, email= "mdaj778866@gmail.com", password= generate_password_hash("admin1234"))
        db.session.add(admin)
        db.session.commit()

app = create_app()

with app.app_context():
    setup_database()



if __name__ == "__main__":
    app.run()
