from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "admin"
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str


class TaiKhoanResponse(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True
