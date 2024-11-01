from flask import Flask
from config import config
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from database import db

db = SQLAlchemy(session_options={"expire_on_commit": False})

def create_app(config_name='development'):
    app = Flask(__name__,template_folder='templates')
    CORS(app, supports_credentials=True)
    bcrypt = Bcrypt(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app