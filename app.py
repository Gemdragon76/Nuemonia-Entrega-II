import sys
import warnings
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# Suprimir advertencias de TensorFlow/Keras (opcional)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=Warning)

from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np

# Cargar el modelo entrenado
model = load_model(r'mi_modelo_entrenado.h5')

# Compilar el modelo con una configuración de compilación genérica
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Ajustar la ruta de la imagen de ejemplo aquí con doble barra diagonal o prefijo r
example_image_path = (r"C:\Users\MMDDB\Downloads\person1710_bacteria_4526.jpeg")

# Función para cargar la imagen de ejemplo y compilar las métricas
def load_example_image():
    try:
        img = tf.keras.preprocessing.image.load_img(example_image_path, target_size=(150, 150))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar la imagen
        return img_array
    except Exception as e:
        print(f"Error al cargar la imagen de ejemplo: {str(e)}")
        return None

# Función para predecir neumonía en una imagen dada
def predict_pneumonia(image_path):
    try:
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar la imagen
        predictions = model.predict(img_array)
        return 'Pneumonia' if predictions[0] > 0.5 else 'No Pneumonia'
    except Exception as e:
        print(f"Error durante la predicción: {str(e)}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <ruta_de_la_imagen>"+ str(sys.argv))
        sys.exit(1)

    image_path = sys.argv[1]
    
    # Cargar ejemplo de imagen para compilar métricas
    example_image = load_example_image()
    
    # Verificar que el ejemplo de imagen no sea None
    if example_image is None:
        print("Error al cargar la imagen de ejemplo.")
        sys.exit(1)
    
    try:
        # Imprimir mensaje indicando que las métricas se están construyendo
        print("Compilando las métricas mediante la evaluación de la imagen de ejemplo...")
        
        # Evaluar el modelo con la imagen de ejemplo
        evaluation_result = model.evaluate(example_image, np.array([1]))  # Proporcionar una etiqueta dummy
        print("Métricas evaluadas:", evaluation_result)
        
        # Realizar la predicción con la imagen proporcionada por el usuario
        prediction = predict_pneumonia(image_path)
        if prediction is not None:
            print(f'Predicción: {prediction}')
        else:
            print("Error: No se pudo hacer la predicción.")
    
    except Exception as e:
        print(f"Error durante la evaluación o predicción: {str(e)}")

