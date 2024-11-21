from flask import request, jsonify, session, Blueprint
from database.models import Users
from database import db
from flask_bcrypt import Bcrypt

login_register_bp = Blueprint('login_register', __name__)
bcrypt = Bcrypt()

@login_register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()  
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'El nombre de usuario ya existe'}), 400
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'El correo electronico ya esta registrado'}), 400
    
    new_user = Users(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200

# Ruta para manejar el inicio de sesión
@login_register_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recibe los datos en formato JSON
    email = data.get('email')
    password = data.get('password')
    
    # Verificar si el usuario existe en la base de datos
    user = Users.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({'message': 'El usuario no existe'}), 401  # Usuario no encontrado
    
    # Verificar si la contraseña es correcta
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Las credenciales no coinciden'}), 401  # Contraseña incorrecta
    
    session['logged_in'] = True  
    
    # Si las credenciales son correctas, iniciar sesión
    session['user_id'] = user.id
    return jsonify({'message': 'Inicio de sesion exitoso'}), 200

@login_register_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Cierre de sesion exitoso'}), 200

@login_register_bp.route('/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session and session['logged_in']:
        user = Users.query.get(session['user_id'])
        if user is not None:
            return jsonify({'logged_in': True}), 200
    session.clear()
    return jsonify({'logged_in': False}), 200