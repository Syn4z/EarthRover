from image_processing import predict
import os
from PIL import Image
import matplotlib.pyplot as plt

# folder_path = "img/"
folder_path = "../downloaded_images/"
num_images_to_process = 25

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.JPG'))]

# Group the images into sets of three
image_sets = [image_files[i:i+3] for i in range(0, len(image_files), 3)]

# Loop through each set of images
for image_set in image_sets:
    # Create a new figure for each set
    plt.figure(figsize=(15, 5))
    
    # Loop through each image in the set
    for i, image_file in enumerate(image_set):
        # Construct full path to the image
        image_path = os.path.join(folder_path, image_file)
        
        # Run the prediction function on the image
        prediction_result, confidence = predict(image_path)
        
        # Load the image
        image = Image.open(image_path)
        
        # Plot the image
        plt.subplot(1, 3, i+1)
        plt.imshow(image)
        plt.title(f"Prediction: {prediction_result}\nConfidence: {confidence * 100:.2f}%")
        plt.axis('off')
    
    # Adjust layout and display the figure
    plt.tight_layout()
    plt.show()
