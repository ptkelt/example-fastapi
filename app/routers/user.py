from fastapi import Body, FastAPI, HTTPException, Depends, Response, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models,schemas,utils
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)): 
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    users = db.query(models.User).all()
    return users

@router.get("/{id}",  response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"{id} not found")
    return user