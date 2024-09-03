from typing import Union,Any,Optional,Dict,List
from pydantic import BaseModel, Field, create_model , AnyUrl

class UserInfoRequest(BaseModel):
    table: str = Field(..., description="The name of the table to modify")
    action: str = Field(..., description="The action to perform (insert, update, delete)")
    name: Optional[str] = Field(None, description="Name of the user or organization")
    location: Optional[str] = Field(None, description="Location of the user")
    organization_name: Optional[str] = Field(None, description="Organization name for the user")
    profile_pic: Optional[str] = Field(None, description="Profile picture URL for the user")
    category: Optional[str] = Field(None, description="Category of the organization")
    logo_link: Optional[str] = Field(None, description="Logo link of the organization")

class UserInfoResponse(BaseModel):
    status: str = Field(default = None)

class LogoPlacementRequest(BaseModel):
    type: str = Field(default = None)
    userPrompt: str = Field(default = None)
    component: str = Field(default = None)

class LogoPlacementResponse(BaseModel):
    content: str = Field(default = None)
    