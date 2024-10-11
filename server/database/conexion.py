import os
from database.db import db
import sqlite3

def create_db():
    basedir = os.path.abspath(os.path.dirname(__file__))
    conn = sqlite3.connect(os.path.join(basedir, 'database.db'))
    cursor = conn.cursor()
    
    with open('database/schema.sql', 'r') as f:
        sql = f.read()
        try:
            cursor.executescript(sql)
            conn.commit()
            print("Base de datos y tablas creadas con exito")
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")

    conn.close()
    
def init_app(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

