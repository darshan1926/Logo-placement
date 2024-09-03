from typing import Union,Any,Optional,Dict,List
from pydantic import BaseModel, Field, create_model , AnyUrl

class ErrorResponse(BaseModel):
    errorMessage: str = Field(default = None)