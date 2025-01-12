from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# ----- User Schemas -----
class UserBase(BaseModel):
    """
    Base schema for users.
    """
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")

class UserCreate(UserBase):
    """
    Schema for creating a new user. Includes password.
    """
    password: str = Field(..., min_length=8, example="securepassword123")

class UserUpdate(BaseModel):
    """
    Schema for updating user details.
    """
    name: Optional[str] = Field(None, example="Updated John Doe")
    email: Optional[EmailStr] = Field(None, example="updated.john.doe@example.com")
    password: Optional[str] = Field(None, min_length=8, example="newsecurepassword123")

class UserResponse(UserBase):
    """
    Response schema for users.
    """
    id: int

    class Config:
        orm_mode = True
