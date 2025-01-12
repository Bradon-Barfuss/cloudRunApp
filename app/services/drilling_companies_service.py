# app/services/drilling_companies_service.py
from sqlalchemy.orm import Session
from app.models.drilling_company import DrillingCompany
from app.schemas.drilling_company import DrillingCompanyCreate, DrillingCompanyUpdate

# Create a new drilling company
def create_drilling_company(db: Session, company_data: DrillingCompanyCreate):
    new_company = DrillingCompany(**company_data.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

# Get all drilling companies
def get_all_drilling_companies(db: Session):
    return db.query(DrillingCompany).all()

# Get a drilling company by ID
def get_drilling_company(db: Session, company_id: int):
    return db.query(DrillingCompany).filter(DrillingCompany.id == company_id).first()

# Update a drilling company
def update_drilling_company(db: Session, company_id: int, company_data: DrillingCompanyUpdate):
    company = get_drilling_company(db, company_id)
    if not company:
        return None
    for key, value in company_data.dict(exclude_unset=True).items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company

# Delete a drilling company
def delete_drilling_company(db: Session, company_id: int):
    company = get_drilling_company(db, company_id)
    if company:
        db.delete(company)
        db.commit()
        return True
    return False
