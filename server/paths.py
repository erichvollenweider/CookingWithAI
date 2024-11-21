import os

# Directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Rutas para los archivos CSV
CSV_PATHS = {
    "csv_v1": os.path.join(BASE_DIR, 'datasets', 'dataset-v1.csv'),
    "csv_v2": os.path.join(BASE_DIR, 'datasets', 'dataset-v2.csv'),
    "csv_f": os.path.join(BASE_DIR, 'datasets', 'dataset-f.csv'),
    "csv_file_carnes": os.path.join(BASE_DIR, 'datasets', 'dataset-carnes.csv')
}

# Rutas para los modelos
MODEL_PATHS = {
    "model_v1_path": os.path.join(BASE_DIR, 'models', 'modeloEntrenado-v1'),
    "model_v2_path": os.path.join(BASE_DIR, 'models', 'modeloEntrenado-v2'),
    "model_f_path": os.path.join(BASE_DIR, 'models', 'modeloEntrenado-f'),
    "model_carnes_path": os.path.join(BASE_DIR, 'models', 'modeloEntrenadoCarnes'),
}