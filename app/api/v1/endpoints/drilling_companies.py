# app/api/v1/endpoints/drilling_companies.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.drilling_companies_service import (
    create_drilling_company,
    get_all_drilling_companies,
    get_drilling_company,
    update_drilling_company,
    delete_drilling_company
)

from app.schemas.drilling_company import DrillingCompanyCreate, DrillingCompanyUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(company: DrillingCompanyCreate, db: Session = Depends(get_db)):
    return create_drilling_company(db, company)

@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: Session = Depends(get_db)):
    return get_all_drilling_companies(db)

@router.get("/{company_id}", status_code=status.HTTP_200_OK)
def read(company_id: int, db: Session = Depends(get_db)):
    company = get_drilling_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", status_code=status.HTTP_202_ACCEPTED)
def update(company_id: int, company_data: DrillingCompanyUpdate, db: Session = Depends(get_db)):
    updated_company = update_drilling_company(db, company_id, company_data)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(company_id: int, db: Session = Depends(get_db)):
    if not delete_drilling_company(db, company_id):
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}
