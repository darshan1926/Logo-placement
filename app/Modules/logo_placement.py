from PIL import Image
from fastapi import UploadFile
import io


class LogoPlacement:
    def __init__(self, original_image: Image.Image, logo_image: Image.Image):
        self.original_image = self.uploadfile_to_pil(original_image)
        self.logo_image = self.uploadfile_to_pil(logo_image)

    def process_and_save_image(self, logo_position=None) -> bytes:
        if logo_position is None:
            logo_position = (
                self.original_image.width - self.logo_image.width - 20,
                self.original_image.height - self.logo_image.height - 20,
            )

        self.original_image.paste(self.logo_image, logo_position, self.logo_image.convert("RGBA"))

        img_byte_arr = io.BytesIO()
        self.original_image.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue() 
    
    def uploadfile_to_pil(self,upload_file: UploadFile) -> Image.Image:
        image = Image.open(io.BytesIO(upload_file.file.read()))
        return image