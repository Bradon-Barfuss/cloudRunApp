from sqlalchemy import Column, Integer, String
from app.api.dependencies.database import Base

class Operator(Base):
    __tablename__ = 'operators'
    id = Column(Integer, primary_key=True, index=True)

    First_Name = Column(String)
    Last_Name = Column(String)
    Age = Column(Integer)
    Email = Column(String)

