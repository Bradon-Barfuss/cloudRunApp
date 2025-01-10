from pydantic import BaseModel, Field


        
class Drilling_Company(BaseModel):
    Company_Name: str = Field(..., example="Example Drilling Co.")
    Phone: str = Field(..., example="123-456-7890")
    Address_1: str = Field(..., example="123 Example St.")
    description: str = Field(..., example="A leading provider of drilling services.")

class Show_Drilling_Company(BaseModel):
    Company_Name: str
    Phone: str

    class Config():
        from_attributes = True


class Operator(BaseModel):
    First_Name: str
    Last_Name: str
    Age: int
    Email: str

class User(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="securepassword")