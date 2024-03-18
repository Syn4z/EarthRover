from image_processing import predict
import os
from PIL import Image

# folder_path = "img/"
folder_path = "./greenhouse_images/Sanatoasa"
num_images_to_process = 25

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.JPG'))]

# Loop through each image file
for i, image_file in enumerate(image_files[:num_images_to_process]):
    # Construct full path to the image
    image_path = os.path.join(folder_path, image_file)
    
    # Run the prediction function on the image
    prediction_result, confidence = predict(image_path)
    
    # Do something with the prediction result (print it, save it, etc.)
    print(f"Prediction for {image_file}: {prediction_result}, Confidence: {confidence:.2f}")