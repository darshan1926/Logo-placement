import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

def extract_dominant_colors(image: Image.Image, num_colors=5):
    """
    Extract dominant colors from an image using K-means clustering.

    Parameters:
    - image: PIL.Image.Image object.
    - num_colors: int, number of dominant colors to extract.

    Returns:
    - dominant_colors: list of RGB tuples representing dominant colors.
    """
    # Convert PIL image to a NumPy array and ensure it is in RGB format
    image_np = np.array(image.convert('RGB'))  # Convert PIL image to RGB NumPy array

    # Reshape the image to a 2D array of pixels
    pixels = image_np.reshape(-1, 3)

    # Use K-means to cluster pixel colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    # Extract the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    
    # Convert dominant colors to a list of RGB tuples
    dominant_colors = [tuple(color) for color in dominant_colors]
    
    return dominant_colors