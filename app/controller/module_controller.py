from app.pymodels.module_response import UserInfoRequest, UserInfoResponse, LogoPlacementRequest, LogoPlacementResponse, BgColorRequest, BgColorResponse
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
            
    return _response

@log.logError
def logoplacementapi(request : LogoPlacementRequest):

    args = vars(request)

    product_name = args['productName']
    additional_information = args['additionalInformation']
    call_to_action = args['callToAction']
    
    component_rewriter = LogoPlacement()
    _response = None # component_rewriter.component_rewrite(product_name,additional_information,call_to_action)       
    result = LogoPlacementResponse(content = _response , parameters  = args , info = "Success")
            
    return result 


@log.logError
async def bgcolorapi(file: UploadFile = File(...)):
    palette_selection = BgColorGenerator()
    try:
        # Read the uploaded file and convert it to an image
        image_data = await file.read()
        image = Image.open(BytesIO(image_data)).convert("RGB")
        
        # Run the inpainting pipeline to process the image
        img_byte_arr = palette_selection.run_pipeline(image)
        
        # Return the image as a response with the appropriate content type
        return Response(content=img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result