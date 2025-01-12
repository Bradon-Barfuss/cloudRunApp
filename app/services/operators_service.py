# app/services/operator_service.py
from sqlalchemy.orm import Session
from app.models.operator import Operator
from app.schemas.operator import OperatorCreate

# Create a new operator
def create_operator(db: Session, operator_data: OperatorCreate):
    new_operator = Operator(**operator_data.dict())
    db.add(new_operator)
    db.commit()
    db.refresh(new_operator)
    return new_operator

# Get all operators
def get_all_operators(db: Session):
    return db.query(Operator).all()

# Get an operator by ID
def get_operator(db: Session, operator_id: int):
    return db.query(Operator).filter(Operator.id == operator_id).first()

# Delete an operator
def delete_operator(db: Session, operator_id: int):
    operator = get_operator(db, operator_id)
    if operator:
        db.delete(operator)
        db.commit()
        return True
    return False
