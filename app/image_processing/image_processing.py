from PIL import Image
import numpy as np
import tensorflow as tf


# Constants
IMG_SIZE = 256

# Load the model
loaded_model = tf.keras.models.load_model(f'image_processing/tomato_lens_model_36.h5')

class_names = ['Bacterial-Spot',
 'Early-Blight',
 'Healthy',
 'Late-Blight',
 'Leaf-Mold',
 'Mosaic-Virus',
 'Septoria-Leaf-Spot',
 'Target-Spot']

# Define the predict function
def predict(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)  # Add batch dimension

    # Make predictions
    predictions = loaded_model.predict(image_array)

    # Decode the predictions and return the result
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])  # Get the confidence score
    return predicted_class, confidence
