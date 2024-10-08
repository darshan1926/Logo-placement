from app.pymodels.module_response import UserInfoRequest, UserInfoResponse
from app.Modules.user_management import UserData
from app.Modules.logo_placement import LogoPlacement
from app.Modules.bg_replacement import BgColorGenerator
from app.config import settings
from logger import LogManager
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, FastAPI, File, UploadFile, HTTPException, Response, Depends
from app.utils.database import get_db
from typing import Dict
from PIL import Image
from io import BytesIO

log = LogManager()
log.setLogger()


@log.logError
def userinfoapi(request : UserInfoRequest,db: Session = Depends(get_db)):
    crud_operations = UserData(db)
    try:
        _response = crud_operations.modify_record(
            table=request.table,
            action=request.action,
            name=request.name,
            location=request.location,
            organization_name=request.organization_name,
            profile_pic=request.profile_pic,
            category=request.category,
            logo_link=request.logo_link
        )
        return _response, False
    except HTTPException as e:
        return str(e.detail), True

@log.logError
def logoplacementapi(logo: UploadFile, product_image: UploadFile) -> tuple:
    try:
        superimpose_image = LogoPlacement(logo, product_image)
        file_path = superimpose_image.process_and_save_image()
        return file_path, False  # Returning the image file path and a flag (False indicating no error)
    except Exception as e:
        return str(e), True

@log.logError
def bgcolorapi(logo: UploadFile = File(...), product_image: UploadFile = File(...)):
    palette_selection = BgColorGenerator()
    try:  
        # Run the inpainting pipeline with both logo and product images
        _response = palette_selection.run_pipeline(logo, product_image)
        
        return _response, False  # Return False for flag as there is no error
    except Exception as e:
        return str(e), True  # Return error message and set flag to True