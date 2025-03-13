from pydantic import BaseModel, Field
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str = None
    role: str = "user"  # "user", "admin", "super-admin"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
