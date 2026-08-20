from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] =  None
    

class LoginSechma(BaseModel):
    email: EmailStr
    password: str
    
