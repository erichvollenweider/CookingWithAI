from database import db
from datetime import datetime
from flask_bcrypt import Bcrypt

# Definicion de la tabla Users
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    
    chats = db.relationship('Chats', backref='user', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'

    # Verifica si la contraseña es correcta
    def check_password(self, password):
        return Bcrypt.check_password_hash(self.password, password)

class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)