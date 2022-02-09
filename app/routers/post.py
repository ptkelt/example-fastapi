from fastapi import Body, FastAPI, HTTPException, Depends, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models,schemas, oath2
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)): #creates post object from json input
    #cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *", (new_post.title, new_post.content))
    #post = cursor.fetchone()
    #conn.commit()
    post = models.Post(owner_id=current_user.id, **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
   #cursor.execute("SELECT * from posts where id = %s", (str(id)))
   #post = cursor.fetchone()
   post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
   if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
   return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #cursor.execute("DELETE FROM posts where id = %s returning *", (str(id)))
    #deleted = cursor.fetchone()
    #conn.commit()
    deleted = db.query(models.Post).filter(models.Post.id == id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    if deleted.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #cursor.execute("UPDATE posts SET title = %s, content = %s where id = %s RETURNING *", (new_post.title, new_post.content, str(id)))
    #updated = cursor.fetchone()
   # conn.commit()
    updated = db.query(models.Post).filter(models.Post.id == id)
    if not updated.first():
        raise HTTPException(status_code=404, detail=f"{id} not found")
    if updated.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    updated.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return updated.first()
