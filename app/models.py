from sqlalchemy import Column, Integer, String
from .database import Base


class drilling_company(Base):
    __tablename__ = 'drilling_companies'
    Company_ID = Column(Integer, primary_key=True, index=True)
    Company_Name = Column(String)
    Phone = Column(String)
    Address_1 = Column(String)
    description = Column(String)

class operator(Base):
    __tablename__ = 'operators'
    operator_ID = Column(Integer, primary_key=True, index=True)

    First_Name = Column(String)
    Last_Name = Column(String)
    Age = Column(Integer)
    Email = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)