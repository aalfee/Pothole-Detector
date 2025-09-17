# This script requires TensorFlow. If you're in a sandboxed environment that does not support it,
# please run this script locally with TensorFlow installed (pip install tensorflow).

import sys
import os
import argparse
import logging
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

# Command line flags
parser = argparse.ArgumentParser(description='Train a pothole detector')
parser.add_argument('--dry-run', action='store_true', help='Run a quick dry-run (no saving)')
parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train')
parser.add_argument('--batch-size', type=int, default=8, help='Training batch size')
parser.add_argument('--no-save', action='store_true', help="Don't save the trained model or plots")
parser.add_argument('--quiet', action='store_true', help='Reduce logging output')
parser.add_argument('--log-file', type=str, default=None, help='Optional path to a log file')
parser.add_argument('--log-level', type=str, default='INFO', help='Log level: DEBUG, INFO, WARNING, ERROR')
args = parser.parse_args()

# Image data preprocessing
img_size = (128, 128)
batch_size = args.batch_size

# Configure logging
numeric_level = getattr(logging, args.log_level.upper(), logging.INFO)
handlers = [logging.StreamHandler()]
if args.log_file:
    handlers.append(logging.FileHandler(args.log_file))
logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s: %(message)s', handlers=handlers)

log = logging.getLogger(__name__)

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
    log.error(f"Failed to load dataset: {e}")
    sys.exit(1)

# If validation set is empty (tiny dataset), skip validation to avoid
# errors like "The PyDataset has length 0" during training.
try:
    # different keras/tf versions expose sample count as .n or .samples
    val_count = 0
    if 'val_data' in locals() and val_data is not None:
        val_count = getattr(val_data, 'n', None) or getattr(val_data, 'samples', 0)
    if val_count == 0:
        log.warning('No validation images found — continuing without validation set')
        val_data = None
except Exception:
    # If any introspection fails, be conservative and keep val_data as-is
    pass

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
epochs = args.epochs
try:
    if args.dry_run:
        # perform one quick train_on_batch step to validate the pipeline
        if not args.quiet:
            log.info('Performing dry-run (one train_on_batch)...')
        x_batch, y_batch = next(iter(train_data))
        model.train_on_batch(x_batch, y_batch)
        history = None
    else:
        if val_data is None:
            history = model.fit(train_data, epochs=epochs, verbose=(0 if args.quiet else 1))
        else:
            history = model.fit(train_data, validation_data=val_data, epochs=epochs, verbose=(0 if args.quiet else 1))
except Exception as e:
    log.error(f"Training failed: {e}")
    sys.exit(1)

# Save the model
if not args.no_save and not args.dry_run:
    try:
        model.save("pothole_detector.h5")
        if not args.quiet:
            log.info("Model saved successfully as pothole_detector.h5")
    except Exception as e:
        log.error(f"Failed to save model: {e}")
        sys.exit(1)

# Plot training results
if not args.no_save and not args.dry_run and history is not None:
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
        if not args.quiet:
            log.info("Training results plot saved as training_results.png")
    except Exception as e:
        log.warning(f"Failed to create training plots: {e}")

# Load test data
test_dataset_path = os.path.join(os.path.dirname(__file__), "dataset/Dataset/test")

# Verify test dataset path exists and contains data
if not os.path.exists(test_dataset_path):
    log.error(f"Test dataset path {test_dataset_path} does not exist.")
    sys.exit(1)

# Check if test dataset directory has the required structure
if not os.path.isdir(test_dataset_path):
    log.error(f"{test_dataset_path} is not a directory.")
    sys.exit(1)

# Check if test dataset directory contains subdirectories
subdirs = [d for d in os.listdir(test_dataset_path) if os.path.isdir(os.path.join(test_dataset_path, d))]
if len(subdirs) < 2:
    log.error(f"Test dataset directory must contain at least 2 subdirectories (one for each class).")
    sys.exit(1)

#