from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Annotated

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/add_drilling_company', status_code=status.HTTP_201_CREATED)
def create(token: Annotated[str, Depends(oauth2_scheme)],Drilling_Company : schemas.Drilling_Company, db: Session = Depends(get_db)):
    new_company = models.drilling_company(Company_Name = Drilling_Company.Company_Name, Phone = Drilling_Company.Phone, Address_1 = Drilling_Company.Address_1, description = Drilling_Company.description)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

@app.get('/get_all_drilling_companies', status_code=status.HTTP_200_OK, response_model=List[schemas.Show_Drilling_Company])
def get_all_drilling_companies(db: Session = Depends(get_db)):
    return db.query(models.drilling_company).all()

@app.get('/get_drilling_company/{id}', status_code=status.HTTP_200_OK)
def get_drilling_company(id, response: Response, db: Session = Depends(get_db)):
    """
    Get a drilling company by ID

    Raises:
        HTTPExecption: If a company ID is not found

    Returns:
        str: Returns the company name based on the ID
    """
    company_name = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {id} not found")
    return company_name



@app.delete('/delete_drilling_company/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_drilling_company(id, response: Response, db: Session = Depends(get_db)):
    """
    Delete a drilling company by ID

    Raises:
        HTTPException: If the company with the given ID is not found

    Returns:
        str: A message indicating the success of the deletion
    """
    company = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {id} not found")
    db.delete(company)
    db.commit()
    return 'Company deleted successfully'

@app.put('/update_drilling_company/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_drilling_company(id, Drilling_Company: schemas.Drilling_Company, db:Session = Depends(get_db)):
    company = db.query(models.drilling_company).filter(models.drilling_company.Company_ID == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company id: {id} not found")
    company.Company_Name = Drilling_Company.Company_Name
    db.commit()
    db.refresh(company)
    return 'Company updated successfully'


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
