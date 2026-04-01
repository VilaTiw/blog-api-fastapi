from pydantic import BaseModel, Field
from app.core.roles import Role

class UserCreate(BaseModel):
    username: str = Field(..., example="Vitali Lylo")
    email: str = Field(..., example="vitali.lylo@mail.com")
    role: Role = Field(default=Role.USER, example="USER")
    password: str = Field(..., example="secret-password")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: str
    role: Role