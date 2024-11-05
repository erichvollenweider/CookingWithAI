import pytest
from flask import session
from app import app, db
from database.models import Users
from app import bcrypt

@pytest.fixture
def client():
    app.config.from_object('config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_success(client):
    data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testpassword"
    }
    response = client.post('/register', json = data)
    assert response.status_code == 200
    assert b"Usuario registrado exitosamente" in response.data

def test_register_existing_username(client):
    password_bc = bcrypt.generate_password_hash("testpassword").decode('utf-8')
    user = Users(username="testuser", email="testuser@gmail.com", password=password_bc)
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    
    data = {
        "username": "testuser",
        "email": "user@gmail.com",
        "password": "password"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert b"El nombre de usuario ya existe" in response.data

def test_register_existing_email(client):
    password_bc = bcrypt.generate_password_hash("testpassword").decode('utf-8')
    user = Users(username="testuser", email="testuser@gmail.com", password=password_bc)
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    
    data = {
        "username": "user",
        "email": "testuser@gmail.com",
        "password": "password"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert b"El correo electronico ya esta registrado" in response.data
    
def test_login_success(client):
    password_bc = bcrypt.generate_password_hash("testpassword").decode('utf-8')
    user = Users(username="testuser", email="testuser@gmail.com", password=password_bc)

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    data = {
        "email": "testuser@gmail.com",
        "password": "testpassword"
    }
    response = client.post('/login', json=data)

    assert response.status_code == 200
    assert b"Inicio de sesion exitoso" in response.data


def test_login_user_not_exist(client):
    data = {
        "email": "user@gmail.com",
        "password": "password"
    }
    response = client.post('/login', json=data)

    assert response.status_code == 401
    assert b"El usuario no existe" in response.data


def test_login_incorrect_password(client):
    password_bc = bcrypt.generate_password_hash("testpassword").decode('utf-8')
    user = Users(username="testuser", email="testuser@gmail.com", password=password_bc)

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    data = {
        "email": "testuser@gmail.com",
        "password": "wrongpassword"
    }
    response = client.post('/login', json=data)

    assert response.status_code == 401
    assert b"Las credenciales no coinciden" in response.data
    
def test_logout(client):
    password_bc = bcrypt.generate_password_hash("testpassword").decode('utf-8')
    user = Users(username="testuser", email="testuser@gmail.com", password=password_bc)

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    data = {
        "email": "testuser@gmail.com",
        "password": "testpassword"
    }
    client.post('/login', json=data)

    response = client.post('/logout')

    assert response.status_code == 200
    assert b"Cierre de sesion exitoso" in response.data

    with app.app_context():
        assert session.get('logged_in', False) is False
        assert 'user_id' not in session


