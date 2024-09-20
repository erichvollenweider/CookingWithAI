import json
import psycopg2
from flask_sqlalchemy import SQLAlchemy

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

# Carga la configuracions desde un JSON
def get_config():
    with open('database/config.json') as f:
        config = json.load(f)
    return config['database']

# Crea la bdd si es que no existe ya, y las tablas necesarias
def create_db():
    config = get_config()
    # Conexion a la bdd
    conn = psycopg2.connect(
        host=config["host"],
        user=config["username"],
        password=config["password"],
        database=config["database"]
    )
    # Crea un cursor para ejecutar queries
    cursor = conn.cursor()
    # Lee el script SQL para crear las tablas
    with open('database/init_db.sql', 'r') as f:
        sql = f.read()
        try:
            # Ejecuta el script SQL
            cursor.execute(sql)
            conn.commit()
            print("Tabla creada con éxito")
        except psycopg2.errors.DuplicateTable:
            print("La tabla ya existe")
    conn.close()

def init_app(app):
    config = get_config()
    # Configura la bdd
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["username"]}:{config["password"]}@{config["host"]}/{config["database"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)