from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, DeleteUser
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user
)


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, tags=["Users"], summary="Create a new user", description="Create a new user with the provided details.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user

@router.get('/', status_code=status.HTTP_200_OK, tags=["Users"], summary="Get all users", description="Retrieve a list of all users.")
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, tags=["Users"], summary="Get a user by ID", description="Retrieve a user by their ID.")
def get_user(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Users"], summary="Update a user", description="Update the details of a user by their ID.")
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, id)
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
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    db.delete(user)
    db.commit()
    return 'User deleted successfully'
