import os
import sys
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np

# Load the trained model
try:
    model = tf.keras.models.load_model("pothole_detector.h5")
    print("Model loaded successfully.")
except Exception as e:
    print(f"ERROR: Failed to load model: {e}")
    sys.exit(1)

# Define test dataset directory
test_dataset_path = os.path.join(os.path.dirname(__file__), "dataset/Dataset/test")

# Verify test dataset path exists and contains data
if not os.path.exists(test_dataset_path):
    print(f"ERROR: Test dataset path {test_dataset_path} does not exist.")
    sys.exit(1)

# Check if test dataset directory has the required structure
if not os.path.isdir(test_dataset_path):
    print(f"ERROR: {test_dataset_path} is not a directory.")
    sys.exit(1)

# Check if test dataset directory contains subdirectories
subdirs = [d for d in os.listdir(test_dataset_path) if os.path.isdir(os.path.join(test_dataset_path, d))]
if len(subdirs) < 2:
    print(f"ERROR: Test dataset directory must contain at least 2 subdirectories (one for each class).")
    sys.exit(1)

# Image data preprocessing
img_size = (128, 128)
batch_size = 32

datagen = ImageDataGenerator(rescale=1./255)

# Load test data
test_data = datagen.flow_from_directory(
    test_dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='binary'
)

# Evaluate the model on test data
try:
    test_loss, test_accuracy = model.evaluate(test_data)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
except Exception as e:
    print(f"ERROR: Testing failed: {e}")
    sys.exit(1)

# Function to display images with predictions
def display_predictions(model, test_data, num_images=5):
    # Get a batch of images and labels
    images, labels = next(test_data)
    predictions = model.predict(images)
    
    # Plot the images with predictions
    plt.figure(figsize=(15, 5))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(images[i])
        plt.title(f"Pred: {'Pothole' if predictions[i] > 0.5 else 'No Pothole'}\nTrue: {'Pothole' if labels[i] == 1 else 'No Pothole'}")
        plt.axis('off')
    plt.show()

# Display a few test images with predictions
display_predictions(model, test_data) 