import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

def extract_dominant_colors(image: Image.Image, num_colors=5):
    image_np = np.array(image.convert('RGB'))
    pixels = image_np.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_.astype(int)
    dominant_colors = [tuple(color) for color in dominant_colors]
    
    return dominant_colors