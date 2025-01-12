from pydantic import BaseModel, Field
from typing import Optional

# ----- Drilling Company Schemas -----
class DrillingCompanyBase(BaseModel):
    """
    Base schema for drilling companies, shared fields for create, update, and response models.
    """
    Company_Name: str = Field(..., example="Example Drilling Co.")
    Phone: str = Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$", example="123-456-7890")
    Address_1: str = Field(..., example="123 Example St.")
    description: Optional[str] = Field(None, example="A leading provider of drilling services.")

class DrillingCompanyCreate(DrillingCompanyBase):
    """
    Schema for creating a new drilling company.
    """
    pass

class DrillingCompanyUpdate(BaseModel):
    """
    Schema for updating an existing drilling company. Optional fields for partial updates.
    """
    Company_Name: Optional[str] = Field(None, example="Updated Drilling Co.")
    Phone: Optional[str] = Field(None, pattern=r"^\d{3}-\d{3}-\d{4}$", example="123-456-7890")
    Address_1: Optional[str] = Field(None, example="456 Updated St.")
    description: Optional[str] = Field(None, example="Updated description.")

class DrillingCompanyResponse(DrillingCompanyBase):
    """
    Response schema for drilling companies.
    """
    id: int

    class Config:
        orm_mode = True