import os
import numpy as np
import pandas as pd
import tensorflow as tf
from paths import MODEL_PATHS, CSV_PATHS

def cargar_csv(archivo_csv):
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        print(f"CSV {archivo_csv} cargado correctamente.")
        return df
    else:
        print(f"El archivo CSV {archivo_csv} no se encuentra en la ruta: {archivo_csv}")
        raise FileNotFoundError(f"El archivo CSV {archivo_csv} no se encuentra en la ruta: {archivo_csv}")

# Se cargan los csvs
df_v1 = cargar_csv(CSV_PATHS["csv_v1"])
df_v2 = cargar_csv(CSV_PATHS["csv_v2"])
df_f = cargar_csv(CSV_PATHS["csv_f"])
df_carnes = cargar_csv(CSV_PATHS["csv_file_carnes"])

class_labels_v1 = df_v1.columns[1:]
class_labels_v2 = df_v2.columns[1:]
class_labels_f = df_f.columns[1:]
class_labels_carnes = df_carnes.columns[1:]

# Se cargan los modelos
def cargar_modelo(modelo_path):
    if os.path.exists(modelo_path):
        print(f'La ruta {modelo_path} es válida y existe.')
        model = tf.keras.models.load_model(modelo_path)
        print(f"Modelo cargado correctamente desde {modelo_path}.")
        return model
    else:
        print(f'La ruta {modelo_path} no existe o es incorrecta.')
        raise FileNotFoundError(f'La ruta {modelo_path} no existe o es incorrecta.')

# Se cargan los modelos
model_v1 = cargar_modelo(MODEL_PATHS["model_v1_path"])
model_v2 = cargar_modelo(MODEL_PATHS["model_v2_path"])
model_f = cargar_modelo(MODEL_PATHS["model_f_path"])
model_carnes = cargar_modelo(MODEL_PATHS["model_carnes_path"])

def preprocess_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')

        
    # Redimensiando la imagen
    image = image.resize((224, 224))
    
    # Convertiendo la imagen a un arreglo
    img_array = np.array(image)
    
    # Asegurando que la imagen tenga las dimensiones correctas (224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalizando
    img_array = img_array / 255.0
    
    return img_array

def mostrar_predicciones(predictions, predicted_labels, labels, label_name):
    print(f"Predicciones {label_name}: ")
    
    # Imprimir las predicciones en formato texto
    predictions_text = [f"{label}: {pred:.2f}" for label, pred in zip(labels, predictions[0])]
    print(", ".join(predictions_text))
    
    # Imprimir las etiquetas predichas
    predicted_labels_text = [label for label, pred in zip(labels, predicted_labels[0]) if pred == 1]
    print(f"Etiquetas predichas {label_name}:", ", ".join(predicted_labels_text))
    print("-----------------------------------------------------------------------------------------------------")

def get_ingredients_from_image(image):
    img_array = preprocess_image(image)
    predictions_v1 = model_v1.predict(img_array)
    predictions_v2 = model_v2.predict(img_array)
    predictions_f = model_f.predict(img_array)
    predictions_carnes = model_carnes.predict(img_array)
    
    # Obtener las etiquetas predichas usando un umbral
    predicted_labels_v1 = (predictions_v1 > 0.6).astype(int)
    predicted_labels_v2 = (predictions_v2 > 0.85).astype(int)
    predicted_labels_f = (predictions_f > 0.7).astype(int)
    predicted_labels_carnes = (predictions_carnes > 0.85).astype(int)

    labels_v1 = ["anquito", "apio", "berenjena", "cebolla", "cebolla morada", "choclo", "coliflor", 
                "huevo", "lechuga", "papa", "pimiento amarillo", "pimiento rojo", "pimiento verde", "remolacha"]
    labels_v2 = ["ajo","arveja", "batata", "brocoli", "cebolla de verdeo", "espinaca", "palta", "pepino","rabanito", "repollo morado",
                "tomate","zanahoria", "zapallito"]
    labels_f = ["aceituna", "ananá", "banana", "cereza", "durazno", "frutilla", "jengibre", "kiwi", "limón", "manzana", "naranja", "pera", "sandía"]
    labels_c = ["alita", "chinchulin", "chorizo", "costeleta de cerdo", "hamburguesa", "milanesa", "morcilla", "pan", "pata-muslo", "pechuga", "pollo", "riñon"]
    
    mostrar_predicciones(predictions_v1, predicted_labels_v1, labels_v1, "verduras V1")
    mostrar_predicciones(predictions_v2, predicted_labels_v2, labels_v2, "verduras V2")
    mostrar_predicciones(predictions_f, predicted_labels_f, labels_f, "frutas")
    mostrar_predicciones(predictions_carnes, predicted_labels_carnes, labels_c, "carnes")
    
    # Concatenar etiquetas y predicciones en una sola lista para simplificar
    all_labels = list(class_labels_v1) + list(class_labels_v2) + list(class_labels_f) + list(class_labels_carnes)
    all_predictions = np.concatenate([predicted_labels_v1[0], predicted_labels_v2[0], predicted_labels_f[0], predicted_labels_carnes[0]])

    # Obtener ingredientes en una sola línea
    ingredients = [all_labels[i] for i in range(len(all_predictions)) if all_predictions[i] == 1]
    return ingredients


def parse_receta(generated_text):
    titulo = ''
    # Filtrar solo el titulo
    try:
        if "Titulo" in generated_text:
            titulo = generated_text.split("Titulo:")[1].split("Ingredientes:")[0].strip()
        else:
            titulo = generated_text.split('\n')[0].strip()
    except IndexError as e:
        print(f"Error al analizar el texto generado: {e}")

    return titulo