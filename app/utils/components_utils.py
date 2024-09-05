import io
import cv2
from fastapi import HTTPException, UploadFile
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

from logger import LogManager

log = LogManager()
log.setLogger()

def extract_dominant_colors(image, num_colors=5):
    image_np = np.array(image.convert('RGB'))
    pixels = image_np.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_.astype(int)
    dominant_colors = [tuple(color) for color in dominant_colors]
    
    return dominant_colors

@log.logError
def uploadfile_to_pil(upload_file: UploadFile) -> Image.Image:
    try:
        contents = upload_file.file.read()
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Verify the image is valid
        upload_file.file.seek(0)  # Reset file pointer to the beginning

        # Convert image to RGB mode if it is not already in RGB
        image = Image.open(io.BytesIO(contents))  # Re-open the image from the byte stream
        image = image.convert("RGB")

        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.")