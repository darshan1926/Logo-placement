import io
import tempfile
from PIL import Image
from fastapi import UploadFile
from matplotlib import pyplot as plt

from app.utils.components_utils import uploadfile_to_pil
from logger import LogManager

log = LogManager()
log.setLogger()

@log.logError
class LogoPlacement:
    def __init__(self, original_image: UploadFile, logo_image: UploadFile):
        self.original_image = uploadfile_to_pil(original_image)
        self.logo_image = uploadfile_to_pil(logo_image)

    @log.logError
    def resize_logo(self, size: tuple):
        """Resize the logo to the specified size."""
        if self.logo_image:
            self.logo_image = self.logo_image.resize(size)

    @log.logError
    def process_and_save_image(self, logo_size: tuple = (200, 200), logo_position=None):
        """Resize the logo, paste it onto the original image, and save it to a temporary file."""
        if self.original_image is None or self.logo_image is None:
            raise ValueError("One or both images are not loaded properly.")

        # Resize the logo
        self.resize_logo(logo_size)

        # Set default position to bottom-right corner if not provided
        if logo_position is None:
            logo_position = (
                self.original_image.width - self.logo_image.width - 20,  # 20 pixels from right edge
                self.original_image.height - self.logo_image.height - 20,  # 20 pixels from bottom edge
            )

        # Paste the logo onto the original image with transparency support
        self.original_image.paste(self.logo_image, logo_position, self.logo_image)

        # Display the result
        plt.imshow(self.original_image)
        plt.axis("off")
        plt.show()

        # Save the image to bytes for further processing or returning
        img_byte_arr = io.BytesIO()
        self.original_image.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
