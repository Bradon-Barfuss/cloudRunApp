from sqlalchemy import Column, Integer, String
from .database import Base


class drilling_company(Base):
    __tablename__ = 'drilling_companies'
    Company_ID = Column(Integer, primary_key=True, index=True)
    Company_Name = Column(String)
    Phone = Column(String)
    Address_1 = Column(String)
    description = Column(String)