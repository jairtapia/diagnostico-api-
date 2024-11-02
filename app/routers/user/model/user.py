from pydantic import BaseModel,EmailStr,Field
from datetime import date
from typing import Optional

class UserValidator(BaseModel):
    user_id: Optional[int] = None
    user_name: str 
    last_name_f: str 
    last_name_m: str 
    telefono: str
    user_type: int

    class Config:
        orm_mode = True

class CredentialsValidator(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length= 8)
    class Config():
        orm_mode = True

