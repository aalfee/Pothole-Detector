# This script requires TensorFlow. If you're in a sandboxed environment that does not support it,
# please run this script locally with TensorFlow installed (pip install tensorflow).

import sys
import os
import matplotlib.pyplot as plt

# Check if TensorFlow is installed and import it
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
except ModuleNotFoundError:
    print("ERROR: TensorFlow is not installed. Please install it using 'pip install tensorflow'.")
    sys.exit(1)

# Define dataset directory (change this to your actual path)
dataset_path = os.path.join(os.path.dirname(__file__), "dataset/Dataset/train")

# Verify dataset path exists and contains data
if not os.path.exists(dataset_path):
    print(f"ERROR: Dataset path {dataset_path} does not exist. Please create a 'dataset' directory with subdirectories for each class.")
    sys.exit(1)

# Check if dataset directory has the required structure
if not os.path.isdir(dataset_path):
    print(f"ERROR: {dataset_path} is not a directory.")
    sys.exit(1)

# Check if dataset directory contains subdirectories
subdirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
if len(subdirs) < 2:
    print(f"ERROR: Dataset directory must contain at least 2 subdirectories (one for each class).")
    sys.exit(1)

# Image data preprocessing
img_size = (128, 128)
batch_size = 32

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

try:
    train_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'
    )
except Exception as e:
    print(f"ERROR: Failed to load dataset: {e}")
    sys.exit(1)

# CNN Model
def build_model():
    model = keras.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D(2,2),
        
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(2,2),
        
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.MaxPooling2D(2,2),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = build_model()

# Train the model
epochs = 10
try:
    history = model.fit(train_data, validation_data=val_data, epochs=epochs)
except Exception as e:
    print(f"ERROR: Training failed: {e}")
    sys.exit(1)

# Save the model
try:
    model.save("pothole_detector.h5")
    print("Model saved successfully as pothole_detector.h5")
except Exception as e:
    print(f"ERROR: Failed to save model: {e}")
    sys.exit(1)

# Plot training results
try:
    plt.figure(figsize=(10, 5))
    
    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history.get('accuracy', []), label='Train Accuracy')
    plt.plot(history.history.get('val_accuracy', []), label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    
    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history.get('loss', []), label='Train Loss')
    plt.plot(history.history.get('val_loss', []), label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_results.png')
    print("Training results plot saved as training_results.png")
except Exception as e:
    print(f"WARNING: Failed to create training plots: {e}")

# Load test data
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

#