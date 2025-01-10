from pydantic import BaseModel # Pydantic does data validation
from typing import Optional


        
class Drilling_Company(BaseModel):
    Company_Name: str
    Phone: str
    Address_1: str
    description: Optional[str] = None

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
    name: str
    email: str
    password: str