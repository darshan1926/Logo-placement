import torch
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from diffusers import DiffusionPipeline
from io import BytesIO
from app.config import settings
from app.utils.components_utils import extract_dominant_colors, uploadfile_to_pil
import matplotlib.pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from diffusers.utils import make_image_grid
from fastapi import UploadFile
import io

class BgColorGenerator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # Initialize Stable Diffusion Inpainting Pipeline
        self.sd_model_name = "stabilityai/stable-diffusion-inpainting"
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-inpainting"
        ).to(self.device)
        self.pipe.enable_attention_slicing()

    def create_mask(self, image):
        """
        Create a mask using Canny edge detection.

        Parameters:
        - image: The input image as a NumPy array.

        Returns:
        - mask: The generated mask as a NumPy array.
        """
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

        # Optionally refine the mask (dilate edges for better masking)
        kernel = np.ones((5, 5), np.uint8)
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)

        # Convert mask to RGB format and normalize (0 to 1)
        mask_image = np.expand_dims(edges_dilated, axis=-1)  # Add channel dimension
        mask_image = np.repeat(mask_image, 3, axis=-1)      # Convert grayscale to RGB format
        mask_image = mask_image / 255.0  # Normalize to 0-1

        # Display mask for debugging
        plt.imshow(edges_dilated, cmap='gray')
        plt.axis("off")
        plt.show()

        return mask_image

    def inpaint_image(self, product_image, mask_image, prompt):
        """
        Perform inpainting on the product image using the given mask and prompt.

        Parameters:
        - product_image: The input product image as a PIL Image.
        - mask_image: The mask image as a NumPy array.
        - prompt: Text prompt for inpainting.

        Returns:
        - output: The inpainted image as a PIL Image.
        """
        try:
            # Convert PIL image to a format expected by the pipeline
            product_image = product_image.convert("RGB")
            # Convert mask to PIL image
            mask_image = Image.fromarray((mask_image * 255).astype(np.uint8), mode='RGB')

            # Perform inpainting
            output = self.pipe(prompt=prompt, image=product_image, mask_image=mask_image).images[0]
        except Exception as e:
            print(f"Error during inpainting: {e}")
            return None
        
        # Display inpainted image for debugging
        plt.imshow(output)
        plt.axis("off")
        plt.show()
        
        return output

    def process_image(self, image, prompt):
        """
        Apply mask to the image using Canny edge detection, then perform inpainting.

        Parameters:
        - image: The input image as a PIL Image.
        - prompt: Text prompt for inpainting.

        Returns:
        - inpainted_image: The result of inpainting as a PIL Image.
        """
        # Convert PIL image to NumPy array
        image_np = np.array(image)
        # Generate mask using Canny edge detection
        mask = self.create_mask(image_np)
        # Perform inpainting with the generated mask and prompt
        inpainted_image = self.inpaint_image(image, mask, prompt)
        return inpainted_image

    def run_pipeline(self, logo_image_path, product_image_path):
        """
        Run the entire pipeline from receiving images to producing the inpainted result.

        Parameters:
        - logo_image_path: The path to the logo image.
        - product_image_path: The path to the product image.

        Returns:
        - inpainted_image_bytes: The inpainted image as bytes, suitable for response.
        """
        # Load the images from the paths
        logo_image = uploadfile_to_pil(logo_image_path)
        product_image = uploadfile_to_pil(product_image_path)

        # Extract dominant color from the logo image and use it in the prompt
        bgcolor = extract_dominant_colors(logo_image)
        print("bgcolor : ", bgcolor[0])
        prompt = f"A beautiful product image with a {bgcolor[0]} background"

        # Process the product image with the inpainting pipeline
        inpainted_image = self.process_image(product_image, prompt)

        # Display the result
        if inpainted_image is not None:
            try:
                plt.imshow(inpainted_image)
                plt.axis("off")
                plt.show()
                
                img_byte_arr = io.BytesIO()
                inpainted_image.save(inpainted_image, format='PNG')
                inpainted_image.seek(0)
                return img_byte_arr.getvalue()

            except Exception as e:
                print(f"Error during saving inpainted image: {e}")
                return None
        else:
            print("Failed to generate inpainted image.")
            return None

    def display_images(self, init_image, mask_image, inpainted_image):
        """
        Display the original image, mask, and inpainted image in a grid.

        Parameters:
        - init_image: The original input image as a PIL Image.
        - mask_image: The generated mask as a PIL Image.
        - inpainted_image: The inpainted image as a PIL Image.
        """
        # Convert images to a format suitable for display
        init_image = np.array(init_image)
        mask_image = np.array(mask_image)
        inpainted_image = np.array(inpainted_image)

        # Create a grid to display the images
        grid = make_image_grid([init_image, mask_image, inpainted_image], rows=1, cols=3)
        plt.imshow(grid)
        plt.axis("off")
        plt.show()