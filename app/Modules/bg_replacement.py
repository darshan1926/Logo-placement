import torch
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from diffusers import StableDiffusionInpaintPipeline
from io import BytesIO
from app.config import settings
from app.utils.components_utils import extract_dominant_colors
import matplotlib.pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

class BgColorGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize Segment Anything Model with a pre-trained model
        self.sam_model = self.initialize_sam_model()
        
        # Initialize Stable Diffusion Inpainting Pipeline
        self.sd_model_name = settings.STABLE_DIFFUSION_MODEL
        self.sd_pipe = StableDiffusionInpaintPipeline.from_pretrained(
            self.sd_model_name,
            torch_dtype=torch.float16
        ).to(self.device)

    def initialize_sam_model(self):
        # Use a pre-trained model from segment-anything
        sam = sam_model_registry["vit_h"]()  # You can choose other models like "vit_l" based on your needs
        sam.to(device=self.device)
        mask_generator = SamAutomaticMaskGenerator(sam)
        return mask_generator

    def preprocess_image(self, image: Image.Image):
        return image

    def generate_mask(self, image: Image.Image):
        # Convert image to numpy array
        image_np = np.array(image)
        
        # Generate masks using Segment Anything Model
        masks = self.sam_model.generate(image_np)
        
        # Combine all masks into one by taking the union of all mask regions
        combined_mask = np.zeros_like(image_np[:, :, 0], dtype=np.uint8)
        for mask in masks:
            combined_mask = np.maximum(combined_mask, mask['segmentation'].astype(np.uint8) * 255)
        
        return Image.fromarray(combined_mask)

    def apply_mask(self, original_image: Image.Image, mask: Image.Image):
        original_image = np.array(original_image)
        mask = np.array(mask.convert('L'))
        mask = cv2.resize(mask, (original_image.shape[1], original_image.shape[0]))

        masked_image = cv2.bitwise_and(original_image, original_image, mask=mask)
        return masked_image

    def inpaint_image(self, masked_image, prompt):
        masked_image_pil = Image.fromarray(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        output = self.sd_pipe(prompt=prompt, image=masked_image_pil, mask_image=masked_image_pil.convert('L')).images[0]
        return output

    async def process_image(self, image: Image.Image, prompt):
        mask = self.generate_mask(image)
        masked_image = self.apply_mask(image, mask)
        inpainted_image = self.inpaint_image(masked_image, prompt)
        return inpainted_image

    def run_pipeline(self, logo_image, product_image):
        print("hello i am in the main code!!!!!--------------------------------------------------------------------")
        bgcolor = extract_dominant_colors(logo_image)
        prompt = f"A beautiful product image with a {bgcolor} background"
        inpainted_image = self.process_image(product_image, prompt)

        img_byte_arr = BytesIO()
        inpainted_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return img_byte_arr

