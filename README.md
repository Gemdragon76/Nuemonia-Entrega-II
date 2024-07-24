# Nuemonia-Entrega-II

# Documento Técnico: Sistema de Detección de Neumonía

## 1. Introducción

Este documento proporciona una visión técnica detallada de un Sistema de Detección de Neumonía implementado en Python. El sistema utiliza un modelo de aprendizaje profundo para analizar imágenes de rayos X de tórax y predecir la presencia de neumonía. Consta de dos componentes principales: una aplicación de interfaz de línea de comandos (CLI) y una aplicación de interfaz gráfica de usuario (GUI).

## 2. Componentes del Sistema

### 2.1 Aplicación de Interfaz de Línea de Comandos (CLI) (app.py)

La aplicación CLI proporciona una forma simple de predecir neumonía a partir de una sola imagen utilizando un modelo pre-entrenado.

#### Características Principales:
- Carga un modelo Keras pre-entrenado para la detección de neumonía
- Procesa y normaliza las imágenes de entrada
- Proporciona predicciones sobre si una imagen muestra signos de neumonía

#### Dependencias:
- TensorFlow/Keras
- NumPy
- Pillow (PIL)

#### Funciones Principales:
1. `load_example_image()`: Carga una imagen de ejemplo para la compilación de métricas
2. `predict_pneumonia(image_path)`: Predice neumonía para una imagen dada

#### Uso:
```
python app.py <ruta_de_la_imagen>
```

### 2.2 Aplicación de Interfaz Gráfica de Usuario (GUI) (detector_neumonia.py)

La aplicación GUI proporciona una interfaz amigable para la detección de neumonía, permitiendo a los usuarios cargar imágenes, ver resultados y generar informes.

#### Características Principales:
- Interfaz fácil de usar para cargar y analizar imágenes de rayos X de tórax
- Muestra la imagen original y los resultados de la predicción
- Genera informes PDF y exportaciones CSV de los resultados

#### Dependencias:
- tkinter
- Pillow (PIL)
- NumPy
- TensorFlow/Keras
- ReportLab (para generación de PDF)

#### Clases y Métodos Principales:
1. Clase `App`: Clase principal de la aplicación
   - `load_img_file()`: Carga un archivo de imagen para análisis
   - `run_model()`: Ejecuta el modelo de predicción en la imagen cargada
   - `create_pdf()`: Genera un informe PDF del análisis
   - `save_results_csv()`: Exporta resultados a un archivo CSV

#### Uso:
```
python detector_neumonia.py
```

## 3. Modelo de Aprendizaje Profundo

Ambas aplicaciones utilizan un modelo Keras pre-entrenado para la detección de neumonía.

- Archivo del modelo: `mi_modelo_entrenado.h5`
- Forma de entrada: (150, 150, 3) - Imágenes RGB redimensionadas a 150x150 píxeles
- Salida: Clasificación binaria (Neumonía / No Neumonía)

## 4. Procesamiento de Imágenes

Las imágenes se procesan de la siguiente manera:
1. Se cargan utilizando Pillow o las utilidades de procesamiento de imágenes de Keras
2. Se redimensionan a 150x150 píxeles
3. Se normalizan dividiendo los valores de píxeles por 255.0

## 5. Proceso de Predicción

1. La imagen se carga y se preprocesa
2. La imagen preprocesada se pasa a través del modelo de red neuronal
3. El modelo produce una probabilidad entre 0 y 1
4. Si la probabilidad es > 0.5, la imagen se clasifica como "Neumonía", de lo contrario "No Neumonía"

## 6. Exportación de Datos

### 6.1 Generación de Informes PDF
- Utiliza ReportLab para crear informes PDF estructurados
- Incluye ID del paciente, fecha de análisis, resultado y probabilidad

### 6.2 Exportación CSV
- Exporta información clave en formato CSV
- Incluye ID del paciente, fecha de análisis, resultado, probabilidad y ruta de la imagen

## 7. Pruebas

### 7.1 Pruebas Unitarias (mdb_test_unittest.py)
- Utiliza el framework unittest de Python
- Prueba el método `load_img_file` de la clase `App`

### 7.2 Pruebas Funcionales (test_pytest.py)
- Utiliza el framework pytest
- Prueba la función `predict_pneumonia` con imágenes de muestra

## 8. Consideraciones de Seguridad y Privacidad

- El sistema procesa datos médicos sensibles (imágenes de rayos X)
- Implementar medidas adecuadas de protección de datos en un entorno de producción
- Asegurar el cumplimiento de HIPAA si se implementa en un entorno de atención médica en los Estados Unidos

## 9. Limitaciones y Mejoras Futuras

- El sistema actual utiliza una clasificación binaria (Neumonía / No Neumonía)
- Considerar la implementación de clasificación multiclase para diferentes tipos de neumonía
- Implementar técnicas de aumento de datos para mejorar la robustez del modelo
- Agregar autenticación de usuarios y control de acceso basado en roles para la aplicación GUI
- Implementar registro (logging) para una mejor trazabilidad y depuración

## 10. Conclusión

Este Sistema de Detección de Neumonía proporciona interfaces CLI y GUI para analizar imágenes de rayos X de tórax. Demuestra la aplicación del aprendizaje profundo en el análisis de imágenes médicas, con el potencial de asistir en el diagnóstico de neumonía. El trabajo futuro debería centrarse en mejorar la precisión del modelo, expandir las capacidades del sistema y asegurar el cumplimiento de las regulaciones sanitarias relevantes.

## Nota: 
Los archivos que inician con _doc_ son los resultados de exportar PDF y CSV y el documento word muestra el ejercio Local.

