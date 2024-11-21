# Notebooks de Entrenamiento

Este archivo contiene el resumen de dos notebooks que implementan técnicas de **Deep Learning** para resolver problemas de clasificación de imágenes en diferentes dominios: **carnes y pan** y **verduras y frutas**. A continuación, se describen los principales conceptos y técnicas utilizados.

---

## 🥩🍞 Entrenamiento Carnes y Pan

### Modelo Base
- **Modelo**: MobileNetV2, una red convolucional preentrenada.
- **Función**: Clasificación y reconocimiento de imágenes.
- **Ventaja**: Aprovecha características aprendidas en innumerables imágenes para mejorar la generalización.
- **Configuración**: Las capas del modelo base están congeladas (no entrenables) para evitar sobreajuste.

### Técnicas Implementadas
1. **Aumento de Datos (Data Augmentation)**:
   - Aplicación de transformaciones a las imágenes (rotaciones, escalados, etc.) para mejorar la generalización y evitar el sobreajuste.

2. **Capas Personalizadas**:
   - Capas densas y de dropout.
   - Regularización mediante `kernel_regularizer`.
   - Objetivo: Mejorar la capacidad de predicción y la generalización del dominio en particular.

### Configuración de Entrenamiento
- **Pérdida**: `binary_crossentropy`, adecuada para problemas de clasificación multilabel.
- **Optimización**: `Adam`.
- **Métricas**:
  - Área bajo la curva (AUC).
  - Exactitud (`accuracy`).
  - Precisión y Sensibilidad (`precision`, `recall`).
  - Pérdida (`loss`).

### Callbacks
- **ReduceLROnPlateau**: Ajusta la tasa de aprendizaje cuando el modelo no mejora.
- **EarlyStopping**: Finaliza el entrenamiento cuando no hay mejora en la perdida en validación.

---

## 🥕🍎 Entrenamiento Verduras y Frutas

### Modelo Base
- **Modelo**: MobileNetV2 (idéntico al modelo utilizado en Carnes y Pan).
- **Configuración**: Capas congeladas para mantener las características preentrenadas.

### Técnicas Implementadas
1. **Aumento de Datos (Data Augmentation)**:
   - Transformaciones aplicadas a las imágenes para mejorar la robustez del modelo.

2. **Capas Personalizadas**:
   - Capas densas y de dropout.
   - Objetivo: Similar al de Carnes y Pan, mejorar la capacidad de predicción y la generalización del dominio en particular.


### Configuración de Entrenamiento
- **Pérdida**: `binary_crossentropy` para problemas multilabel.
- **Optimización**: `Adam`.
- **Métricas**:
  - AUC, exactitud, precisión, sensibilidad y pérdida.

### Callbacks
- **ReduceLROnPlateau**: Ajusta la tasa de aprendizaje cuando el modelo no mejora.
- **EarlyStopping**: Finaliza el entrenamiento cuando no hay mejora en la perdida en validación.

---

## 📁 Notebooks Detalladas
Para más detalles, consulta las notebooks en la carpeta `training/`. Cada una contiene explicaciones y resultados específicos.
