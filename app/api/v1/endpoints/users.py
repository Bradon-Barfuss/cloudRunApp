from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user
)
from typing import List
import models
import schemas

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Users"], summary="Create a new user", description="Create a new user with the provided details.")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.User], tags=["Users"], summary="Get all users", description="Retrieve a list of all users.")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User, tags=["Users"], summary="Get a user by ID", description="Retrieve a user by their ID.")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User, tags=["Users"], summary="Update a user", description="Update the details of a user by their ID.")
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

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"], summary="Delete a user", description="Delete a user by their ID.")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    db.delete(user)
    db.commit()
    return 'User deleted successfully'
