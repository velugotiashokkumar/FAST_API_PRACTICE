from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..models import Todos, Users
from ..database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user, bcrypt_context


router = APIRouter(prefix='/user', tags=['user'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class user_password_verification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    
    
@router.get("/read-user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    return db.query(Users).filter(Users.id == user.get("id")).first()

@router.put("/update-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, password_verification: user_password_verification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(password_verification.password, user_model.hassed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The present Password is invalid")
    user_model.hassed_password = bcrypt_context.hash(password_verification.new_password)
    db.add(user_model)
    db.commit()
    
@router.put("/update-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, new_phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()
    