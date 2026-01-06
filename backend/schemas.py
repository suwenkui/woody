from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ApiInfoBase(BaseModel):
    name: str
    description: Optional[str] = None
    detail: Optional[str] = None
    url: str
    method: str

class ApiInfoCreate(ApiInfoBase):
    pass

class ApiInfo(ApiInfoBase):
    id: int

    class Config:
        orm_mode = True
