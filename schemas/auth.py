from pydantic import BaseModel, EmailStr
from uuid import UUID


# ===============================
# Requests
# ===============================
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ===============================
# Responses
# ===============================
class UserInfo(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo
