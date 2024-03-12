import numpy as np
from PIL import Image
import tensorflow as tf


# Preprocess input image
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image = np.array(image) / 255.0
    return image


# Function to predict on an image
def predict(image_path):
    image = preprocess_image(image_path)
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    return prediction


IMG_WIDTH = 256
IMG_HEIGHT = 256

lbls_pred = []
pred_confs = []
class_names = ['Bacterial-spot',
 'Early-blight',
 'Healthy',
 'Late-blight',
 'Leaf-mold',
 'Mosaic-virus',
 'Septoria-leaf-spot',
 'Yellow-leaf-curl-virus']

image_dir = 'img'
model = tf.keras.models.load_model(f'tomato-disease-detection-model.h5')

image_path = f"{image_dir}/tomato_late_blight.JPG"



predictions = predict(image_path)
for prediction in predictions:
            lbls_pred.append(np.argmax(prediction))
            pred_confs.append(np.max(prediction))
            break

lbls_pred_names = list(map(lambda x: class_names[x], lbls_pred))

print("Label number: ", lbls_pred)
print("Confidence: ", round(100 * pred_confs[0], 2))
print("Diagnosis: ", lbls_pred_names)