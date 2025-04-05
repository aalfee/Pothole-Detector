from pymongo import MongoClient
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MongoDB
client = MongoClient("mongodb+srv://bcheng33:Fmmu442xjtumo@cluster0.xbjc5a8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['pothole_db']
collection = db['image_vectors']

# Load pre-trained model
model = VGG16(weights='imagenet', include_top=False)

# Function to extract features from an image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()

# Function to store image vectors in MongoDB
def store_image_vectors(image_dir):
    for img_name in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_name)
        vector = extract_features(img_path)
        collection.insert_one({'image_path': img_path, 'vector': vector.tolist()})
    print("Image vectors stored in MongoDB.")

# Function to find similar images
def find_similar_images(query_vector, top_n=5):
    # Retrieve all vectors from MongoDB
    all_vectors = list(collection.find())
    
    # Calculate cosine similarity
    similarities = []
    for item in all_vectors:
        stored_vector = np.array(item['vector'])
        similarity = cosine_similarity([query_vector], [stored_vector])[0][0]
        similarities.append((item['image_path'], similarity))
    
    # Sort by similarity and get top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar_images = similarities[:top_n]
    
    return top_similar_images

# Example usage
if __name__ == "__main__":
    # Store vectors for images in a directory
    test_dataset_path = os.path.join(os.path.dirname(__file__), "dataset/Dataset/test/Pothole")
    print("store images ------")
    store_image_vectors(test_dataset_path)
    
    print("find similar images ------")
    query_vector = extract_features('1.jpg')
    print("query vector ------")
    similar_images = find_similar_images(query_vector)
    print(similar_images) 