from fastapi import APIRouter, HTTPException, File, UploadFile, Response
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
@log.logError  # Apply the logger decorator
def logo(logo_image: UploadFile = File(...), product_image: UploadFile = File(...)):
    _response, flag = logoplacementapi(logo_image, product_image)
    if flag:
        return ErrorResponse(errorMessage=_response)
    else:
        return Response(content=_response, media_type="image/png")
    
@router.post("/generateCompanyStyleImage")
@log.logError
def bgcolor(logo: UploadFile = File(...), product_image: UploadFile = File(...)):
    _response, flag = bgcolorapi(logo, product_image)
    if flag:
        return ErrorResponse(errorMessage=str(_response))
    else:
        return Response(content=_response, media_type="image/png")