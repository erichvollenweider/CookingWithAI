# 🍰 **Cooking With AI** 

> 🚧 **Proyecto en desarrollo**  
> Este proyecto **NO** está finalizado en su totalidad. ¡Mantente al tanto para futuras actualizaciones y mejoras! 

---

## 👥 **Equipo de desarrollo**
- **Bavera, Guillermo**
- **Bricco, Matias**
- **Conti, Bruno**
- **Gonzalez, Juan Cruz**
- **Mezzano, Joaquin**
- **Vollenweider, Erich**

---

## 📖 **Descripción**
Cooking With AI utiliza **inteligencia artificial** para analizar imágenes de ingredientes alimenticios, identificarlos y generar recetas basadas en ellos. A través del procesamiento de imágenes y modelos de lenguaje, el sistema puede reconocer ingredientes en una foto y sugerir recetas que los incluyan. ¡Así, puedes crear platos deliciosos y adaptados a los ingredientes que ya tienes en casa! 🥕🍅🍲

## 💡 **Motivación**
Este proyecto surge de la necesidad de:
- **Facilitar la planificación de comidas**
- **Reducir el desperdicio alimentario**  

Muchas personas tienen ingredientes en casa, pero no siempre saben cómo combinarlos. Esta aplicación simplifica la creación de recetas, promoviendo una alimentación creativa y evitando que los alimentos se desperdicien. ♻️

## 🎯 **Objetivo**
El objetivo de Cooking With AI es desarrollar una aplicación que permita a los usuarios:
- **Obtener sugerencias de recetas** a partir de los ingredientes detectados en imágenes
- **Aprovechar técnicas de IA** como el reconocimiento de imágenes para ofrecer soluciones prácticas

## 🔧 **Tecnologías utilizadas**
- [Ollama](https://ollama.com) 🧠
- [Python3](https://www.python.org/) 🐍
- [Flask](https://flask.palletsprojects.com/en/stable/) 🌐
- [React](https://es.react.dev/) ⚛️

---

## 🚀 **Instalación (Linux)**
> **Nota**: todos los pasos siguientes deben ejecutarse en la terminal.

### 1. Actualizar el sistema
```bash
sudo apt update && sudo apt upgrade
```

### 2. Instalar las dependencias necesarias
#### 🧰 Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 🐍 Python
```bash
sudo apt install python3 python3-venv python3-pip
```

#### 📦 Node.js
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 3. Instalar el modelo Gemma2 de Ollama
```bash
ollama pull gemma2:2b
```

### 4. Clonar el repositorio
#### Elige la ubicación donde deseas el proyecto y ejecuta:
```bash
git clone https://github.com/erichvollenweider/CookingWithAI.git
```
### 5. Crear el entorno virtual
```bash
cd /ruta/CookingWithAI/server
python3 -m venv .venv
```

### 6. Configurar el entorno virtual
```bash
source .venv/bin/activate
pip install -r requirements.txt
deactivate  # Salida del entorno virtual
```

### 7. Instalar dependencias del cliente (React)
#### En otra terminal, accede al cliente:
```bash
cd /ruta/CookingWithAI/client
npm install
```

## 🏁 **Ejecucción del Proyecto**

### 1. Iniciar el servidor de Ollama
#### Deja esta terminal abierta:
```bash
ollama serve
```

### 2. Iniciar el servidor de Python
#### En otra terminal:
```bash
source .venv/bin/activate
python3 app.py
```
> 💡 **¿Deseas habilitar el RAG?** Haz clic [aquí](#habilitar-rag) para activar esta funcionalidad y luego regresa a este paso para continuar con la ejecución estándar.

### 3. Iniciar el servidor de React
#### En una tercera termina, ejecuta el cliente:
```bash
npm run dev  # Ejecución en localhost
npm run dev -- --host  # Ejecución en localhost y red
```

## 🌐 **Acceder a la aplicacción**
Abre tu navegador e ingresa la dirección IP proporcionada en la consola de NPM. ¡Estás listo para explorar Cooking With AI! 🎉

## 🔎 **Habilitar RAG**
El **RAG (Retrieval-Augmented Generation)** permite integrar capacidades avanzadas de recuperación de información para enriquecer las respuestas de Gemma2 con datos específicos, en este caso para dar recetas argentinas.  

### Pasos para activar el RAG:
#### 1. Descargar el modelo adicional de embeddings:
```bash
ollama pull nomic-embed-text
```

#### 2. Ejecutar el archivo encargado de generar la base de datos con los embeddings:
```bash
python3 gemma2_rag.py
```

#### 3. Regresa al paso correspondiente en la [ejecución del proyecto](#iniciar-el-servidor-de-python) para continuar con la configuración estándar.


