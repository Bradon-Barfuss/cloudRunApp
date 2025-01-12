from sqlalchemy import Column, Integer, String
from app.dependencies.database import Base


class DrillingCompany(Base):
    __tablename__ = 'drilling_companies'
    Company_ID = Column(Integer, primary_key=True, index=True)
    Company_Name = Column(String)
    Phone = Column(String)
    Address_1 = Column(String)
    description = Column(String)