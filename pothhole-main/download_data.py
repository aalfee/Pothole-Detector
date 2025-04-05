import kagglehub

# Download latest version
path = kagglehub.dataset_download("sachinpatel21/pothole-image-dataset")

print("Path to dataset files:", path)