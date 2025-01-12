from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorResponse
from app.models.operator import Operator
from app.services.operators_service import (
    create_operator,
    get_all_operators,
    get_operator,
    update_operator,
    delete_operator
)
from typing import List

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OperatorResponse, tags=["Operators"], summary="Create a new operator", description="Create a new operator with the provided details.")
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    new_operator = Operator(First_Name=operator.First_Name, Last_Name=operator.Last_Name, Age=operator.Age, Email=operator.Email)
    db.add(new_operator)
    db.commit()
    db.refresh(new_operator)
    return new_operator

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[OperatorResponse], tags=["Operators"], summary="Get all operators", description="Retrieve a list of all operators.")
def get_all_operators(db: Session = Depends(get_db)):
    return db.query(Operator).all()

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Operator, tags=["Operators"], summary="Get an operator by ID", description="Retrieve an operator by their ID.")
def get_operator(id: int, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.id == id).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    return operator

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Operator, tags=["Operators"], summary="Update an operator", description="Update the details of an operator by their ID.")
def update_operator(id: int, operator: OperatorUpdate, db: Session = Depends(get_db)):
    db_operator = db.query(Operator).filter(Operator.id == id).first()
    if not db_operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    
    db_operator.First_Name = operator.First_Name
    db_operator.Last_Name = operator.Last_Name
    db_operator.Age = operator.Age
    db_operator.Email = operator.Email
    
    db.commit()
    db.refresh(db_operator)
    return db_operator

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Operators"], summary="Delete an operator", description="Delete an operator by their ID.")
def delete_operator(id: int, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.id == id).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Operator with id {id} not found")
    
    db.delete(operator)
    db.commit()
    return 'Operator deleted successfully'