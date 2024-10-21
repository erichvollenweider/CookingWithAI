# <h1 style="text-align: center"> :cake: Cooking With IA </h1>

> [!NOTE]
> ¡El proyecto NO ha sido finalizado en su totalidad!, se esperan proximas actualizaciones al mismo.

- **Integrantes** 
  - Bavera, Guillermo
  - Bricco, Matias
  - Conti, Bruno
  - Gonzalez, Juan Cruz
  - Mezzano, Joaquin
  - Vollenweider, Erich

- **Descripción:** Este proyecto utiliza inteligencia artificial para analizar imágenes de ingredientes alimenticios, identificarlos y generar recetas basadas en ellos. A través del procesamiento de imágenes y modelos de lenguaje entrenados específicamente, el sistema es capaz de reconocer ingredientes en una foto y sugerir una variedad de recetas que utilizan esos ingredientes, facilitando la creación de platos variados y adaptados a los ingredientes disponibles.

- **Motivación:** Este proyecto surge de la necesidad de facilitar la planificación de comidas y la reducción del desperdicio alimentario. Muchas personas tienen ingredientes en casa pero no saben cómo combinarlos o aprovecharlos. A través de esta aplicación, se simplifica el proceso de creación de recetas, promoviendo una alimentación más creativa y evitando que alimentos se desperdicien por falta de ideas para su uso.

- **Objetivo:** El objetivo del proyecto es desarrollar una aplicación que permita a los usuarios obtener sugerencias de recetas a partir de los ingredientes detectados en imágenes, utilizando técnicas de IA como el reconocimiento de imágenes.

- **Tecnologias utilizadas** 
    - Ollama (IA)
    - Python3 
    - Flask (Microframework de python)
    - SQLAlchemy (Base de datos)
    - JavaScript
    - React (Framework de JavaScript)
    - NodeJS (Se encarga de ejecutar Vite con el comando npm)
    - Vite (Encargado de compilar el código JSX a JavaScript para que el navegador pueda entenderlo)
    - CSS (Estilos)

## Proceso de instalación (Solo Linux) 
Aclaracion: todos los pasos siguientes se ejecutan en la terminal

1. Actualizar el sistema:
	`sudo apt update`
	`sudo apt upgrade`

2. Instalar todas las dependencias necesarias
	`curl -fsSL https://ollama.com/install.sh | sh` Ollama
	`sudo apt install python3 python3-venv python3-pip` Python3 y sus dependencias
	`curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -` Repositorio de Node
	`sudo apt install -y nodejs`

3. Bajamos el modelo a utilizar (Gemma2)
	`ollama pull gemma2:2b` Se instala el modelo gemma2

4. Bajamos el repositorio en la ruta que deseamos
	`git clone https://github.com/erichvollenweider/CookingWithAI.git`

5. Creamos el entorno
	`cd /tu_ruta/CookingWithAI/server` 
	`python3 -m venv venv` Creacion del entorno virtual

6. Accedemos al entorno para configurarlo por primera vez
	`source venv/bin/activate` Activacion del entorno virtual 
	`pip install -r requirements.txt` Instalando requerimientos necesarios para correr la aplicacion
	`deactivate` Salida del entorno virtual.

7. Accedemos en otra terminal nueva (terminal2) a la parte del cliente
	`cd /tu_ruta/CookingWithAI/client`
	`npm install` Instalando dependencias de NodeJS

## Proceso de ejecución (Una vez instalado)
1. Abrimos el servidor de Ollama y lo dejamos abierto (Si es que no se abre automaticamente, ver configuración de cada computadora)
	`ollama serve`

2. Abrimos el servidor de python en terminal1
	`source venv/bin/activate`
	`flask --app app.py run` Ejecucion

3. Abrimos parte del frontend en terminal2
	`npm run dev` Ejecucion 

4. Entramos a la dirección IP que nos provee en la consola NPM (terminal2), utilizando el navegador. Estamos en la aplicacion!
