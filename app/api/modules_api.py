from fastapi import APIRouter, HTTPException, FastAPI, File, UploadFile, HTTPException, Response, Depends
from app.pymodels.module_response import UserInfoRequest, UserInfoResponse, LogoPlacementRequest, LogoPlacementResponse
from app.controller.module_controller import userinfoapi, logoplacementapi, bgcolorapi
from app.pymodels.error_response import ErrorResponse
from typing import Union

router = APIRouter(
    prefix="/tm-api/v1",
    tags=["Image manipulation's"],
)

@router.post("/user-management", response_model=Union[UserInfoResponse, ErrorResponse])
def user_data(request : UserInfoRequest):
    try:
        _response ,flag = userinfoapi(request=request)
        if flag:
            return {"status":ErrorResponse(errorMessage=str(_response))}
        else:
            return {"status":_response}
    except Exception as e:
        return {"status":ErrorResponse(errorMessage=str(e))}

@router.post("/logo-placement", response_model=Union[LogoPlacementResponse,ErrorResponse])
def fetching_image_gen_api(request : LogoPlacementRequest):
    try:
        _response,flag = logoplacementapi(request=request)
        if flag:
            return ErrorResponse(errorMessage=str(_response))
        else:
            return _response
    except Exception as e:
        return ErrorResponse(errorMessage=str(e))
    
@router.post("/bg-generator")
def fetching_color_api(file: UploadFile = File(...)):
    try:
        _response ,flag = bgcolorapi(request=file)
        if flag:
            return ErrorResponse(errorMessage=str(_response))
        else:
            return _response
    except Exception as e:
        return ErrorResponse(errorMessage=str(e))