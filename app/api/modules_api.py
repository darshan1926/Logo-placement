from fastapi import APIRouter, HTTPException, File, UploadFile, Response
from fastapi.responses import FileResponse
from app.pymodels.module_response import UserInfoRequest, UserInfoResponse
from app.controller.module_controller import userinfoapi, logoplacementapi, bgcolorapi
from app.pymodels.error_response import ErrorResponse
from typing import Union
from logger import LogManager

log = LogManager()
log.setLogger()

router = APIRouter(
    prefix="/tm-api/v1",
    tags=["Image manipulation's"],
)

@router.post("/userManagement", response_model=Union[UserInfoResponse, ErrorResponse])
@log.logError  # Apply the logger decorator
def user_data(request: UserInfoRequest):
    _response, flag = userinfoapi(request=request)
    if flag:
        return {"status": ErrorResponse(errorMessage=str(_response))}
    else:
        return {"status": _response}

@router.post("/generateUserProfile")
@log.logError
def logo(logo_image: UploadFile = File(...), product_image: UploadFile = File(...)):
    try:
        file_path, flag = logoplacementapi(logo_image, product_image)
        if flag:
            raise HTTPException(status_code=500, detail=file_path)
        # Send the image file directly
        return FileResponse(file_path, media_type="image/png", filename="output_image.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/generateCompanyStyleImage")
@log.logError
def bgcolor(logo: UploadFile = File(...), product_image: UploadFile = File(...)):
    try:
        _response, flag = bgcolorapi(logo, product_image)
        if flag:
            raise HTTPException(status_code=500, detail=_response)
        return Response(content=_response, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))