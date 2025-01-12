from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# ----- Operator Schemas -----
class OperatorBase(BaseModel):
    """
    Base schema for operators.
    """
    First_Name: str = Field(..., example="Jane")
    Last_Name: str = Field(..., example="Doe")
    Age: int = Field(..., ge=18, le=65, example=30)  # Age constraint between 18 and 65
    Email: EmailStr = Field(..., example="jane.doe@example.com")

class OperatorCreate(OperatorBase):
    """
    Schema for creating a new operator.
    """
    pass

class OperatorUpdate(BaseModel):
    """
    Schema for updating an operator.
    """
    First_Name: Optional[str] = Field(None, example="Updated Jane")
    Last_Name: Optional[str] = Field(None, example="Updated Doe")
    Age: Optional[int] = Field(None, ge=18, le=65, example=35)
    Email: Optional[EmailStr] = Field(None, example="updated.jane.doe@example.com")

class OperatorResponse(OperatorBase):
    """
    Response schema for operators.
    """
    id: int

    class Config:
        from_attributes = True