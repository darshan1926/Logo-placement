import torch
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from diffusers import StableDiffusionInpaintPipeline
from io import BytesIO
from app.config import settings 
from app.utils.components_utils import extract_dominant_colors
class BgColorGenerator:
    def __init__(self):
        # Initialize SAM Model
        self.sam_model = self.load_sam_model(settings.SAM_MODEL)
        self.sd_model_name=settings.STABLE_DIFFUSION_MODEL
        
        # Initialize Stable Diffusion Inpainting Model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sd_pipe = StableDiffusionInpaintPipeline.from_pretrained(
            self.sd_model_name, 
            torch_dtype=torch.float16
        ).to(self.device)
    
    def load_sam_model(self, model_path):
        # Load the pre-trained SAM model
        model = torch.load(model_path)
        model.eval()
        return model
    
    def preprocess_image(self, image: Image.Image):
        """Preprocess the input image."""
        return image
    
    def generate_mask(self, image: Image.Image):
        """Generate mask using SAM model."""
        preprocess = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])
        input_image = preprocess(image).unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():
            output = self.sam_model(input_image)
        
        # Post-process the output to obtain the mask
        mask = output[0].cpu().numpy()  # Convert to numpy array
        mask = (mask > 0.5).astype(np.uint8) * 255  # Binary mask
        
        return Image.fromarray(mask[0])  # Convert numpy array to PIL Image
    
    def apply_mask(self, original_image: Image.Image, mask: Image.Image):
        """Apply mask to the original image."""
        original_image = np.array(original_image)
        mask = np.array(mask.convert('L'))  # Convert PIL mask to grayscale numpy array
        mask = cv2.resize(mask, (original_image.shape[1], original_image.shape[0]))
        
        # Create masked image
        masked_image = cv2.bitwise_and(original_image, original_image, mask=mask)
        return masked_image
    
    def inpaint_image(self, masked_image, prompt="A beautiful landscape"):
        """Perform inpainting using Stable Diffusion."""
        # Convert masked image to PIL format for Stable Diffusion
        masked_image_pil = Image.fromarray(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        
        # Inpainting
        masked_image = np.array(masked_image_pil)
        output = self.sd_pipe(prompt=prompt, image=masked_image, mask_image=np.array(masked_image_pil.convert('L'))).images[0]
        return output
    
    def process_image(self, image: Image.Image, prompt):
        """Process the image with SAM-based masking and Stable Diffusion inpainting."""
        # Generate mask
        mask = self.generate_mask(image)
        
        # Apply the mask to the original image
        masked_image = self.apply_mask(image, mask)
        
        # Perform inpainting
        inpainted_image = self.inpaint_image(masked_image, prompt)
        
        return inpainted_image

    def run_pipeline(self, image: Image.Image):
        """Call all functions to process the image and return the result as bytes."""
        bgcolor = extract_dominant_colors(image)
        prompt=f"generate the {bgcolor} "
        # Process the image through the pipeline
        inpainted_image = self.process_image(image, prompt)
        
        # Convert the inpainted image to bytes
        img_byte_arr = BytesIO()
        inpainted_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return img_byte_arr
