from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Annotated
import logging

app = FastAPI(
    openapi_tags=[
        {
            "name": "Drilling Companies",
            "description": "Operations related to drilling companies."
        },
        {
            "name": "Users",
            "description": "Operations related to user management."
        },
        {
            "name": "Operators",
            "description": "Operations related to operators."
        }
    ]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/add_drilling_company', status_code=status.HTTP_201_CREATED, tags=["Drilling Companies"], summary="Add a new drilling company", description="Create a new drilling company with the provided details.")
def create(token: Annotated[str, Depends(oauth2_scheme)], Drilling_Company: schemas.Drilling_Company, db: Session = Depends(get_db)):
    logger.info("Creating a new drilling company")
    new_company = models.drilling_company(Company_Name=Drilling_Company.Company_Name, Phone=Drilling_Company.Phone, Address_1=Drilling_Company.Address_1, description=Drilling_Company.description)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    logger.info(f"Drilling company {new_company.Company_Name} created successfully")
    return new_company

@app.get('/get_all_drilling_companies', status_code=status.HTTP_200_OK, response_model=List[schemas.Show_Drilling_Company], tags=["Drilling Companies"], summary="Get all drilling companies", description="Retrieve a list of all drilling companies.")
def get_all_drilling_companies(db: Session = Depends(get_db)):
    return db.query(models.drilling_company).all()

@app.get('/get_drilling_company/{id}', status_code=status.HTTP_200_OK, tags=["Drilling Companies"], summary="Get a drilling company by ID", description="Retrieve a drilling company by its ID.")
def get_drilling_company(id, response: Response, db: Session = Depends(get_db)):
    company_name = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {id} not found")
    return company_name

@app.delete('/delete_drilling_company/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Drilling Companies"], summary="Delete a drilling company", description="Delete a drilling company by its ID.")
def delete_drilling_company(id, response: Response, db: Session = Depends(get_db)):
    company = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {id} not found")
    db.delete(company)
    db.commit()
    return 'Company deleted successfully'

@app.put('/update_drilling_company/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Drilling Companies"], summary="Update a drilling company", description="Update the details of a drilling company by its ID.")
def update_drilling_company(id, Drilling_Company: schemas.Drilling_Company, db: Session = Depends(get_db)):
    company = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company id: {id} not found")
    company.Company_Name = Drilling_Company.Company_Name
    db.commit()
    db.refresh(company)
    return 'Company updated successfully'

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Users"], summary="Create a new user", description="Create a new user with the provided details.")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[schemas.User], tags=["Users"], summary="Get all users", description="Retrieve a list of all users.")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User, tags=["Users"], summary="Get a user by ID", description="Retrieve a user by their ID.")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User, tags=["Users"], summary="Update a user", description="Update the details of a user by their ID.")
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"], summary="Delete a user", description="Delete a user by their ID.")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    db.delete(user)
    db.commit()
    return 'User deleted successfully'

@app.post('/operator', status_code=status.HTTP_201_CREATED, response_model=schemas.Operator, tags=["Operators"], summary="Create a new operator", description="Create a new operator with the provided details.")
def create_operator(operator: schemas.Operator, db: Session = Depends(get_db)):
    new_operator = models.Operator(First_Name=operator.First_Name, Last_Name=operator.Last_Name, Age=operator.Age, Email=operator.Email)
    db.add(new_operator)
    db.commit()
    db.refresh(new_operator)
    return new_operator

@app.get('/operators', status_code=status.HTTP_200_OK, response_model=List[schemas.Operator], tags=["Operators"], summary="Get all operators", description="Retrieve a list of all operators.")
def get_all_operators(db: Session = Depends(get_db)):
    return db.query(models.Operator).all()

@app.get('/operator/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Operator, tags=["Operators"], summary="Get an operator by ID", description="Retrieve an operator by their ID.")
def get_operator(id: int, db: Session = Depends(get_db)):
    operator = db.query(models.Operator).filter(models.Operator.id == id).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    return operator

@app.put('/operator/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Operator, tags=["Operators"], summary="Update an operator", description="Update the details of an operator by their ID.")
def update_operator(id: int, operator: schemas.Operator, db: Session = Depends(get_db)):
    db_operator = db.query(models.Operator).filter(models.Operator.id == id).first()
    if not db_operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    
    db_operator.First_Name = operator.First_Name
    db_operator.Last_Name = operator.Last_Name
    db_operator.Age = operator.Age
    db_operator.Email = operator.Email
    
    db.commit()
    db.refresh(db_operator)
    return db_operator

@app.delete('/operator/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Operators"], summary="Delete an operator", description="Delete an operator by their ID.")
def delete_operator(id: int, db: Session = Depends(get_db)):
    operator = db.query(models.Operator).filter(models.Operator.id == id).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    
    db.delete(operator)
    db.commit()
    return 'Operator deleted successfully'