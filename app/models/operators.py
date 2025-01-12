from sqlalchemy import Column, Integer, String
from .database import Base

class operator(Base):
    __tablename__ = 'operators'
    operator_ID = Column(Integer, primary_key=True, index=True)

    First_Name = Column(String)
    Last_Name = Column(String)
    Age = Column(Integer)
    Email = Column(String)

