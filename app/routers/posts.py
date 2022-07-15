from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostWithLikes])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
                  skip: int = 0, search: Optional[str] = ""):
    # all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    all_posts = db.query(models.Post, func.count(models.Likes.post_id).label("likes")).join(models.Likes,
                                                                                            models.Likes.post_id == models.Post.id,
                                                                                            isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return all_posts


@router.get("/current_user", response_model=List[schemas.PostCurrentUser])
def get_all_posts_created_by_current_user(db: Session = Depends(get_db),
                                          current_user: int = Depends(oauth2.get_current_user)):
    all_posts_created_by_current_user = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return all_posts_created_by_current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCurrentUser)
def create_post(new_post_data: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**new_post_data.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts_id_container = db.query(models.Post.id).all()
    if len(posts_id_container) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Latest post not found.")
    max_id = 0
    for i in posts_id_container:
        for j in i:
            if j > max_id:
                max_id = j
    latest_post = db.query(models.Post).filter(models.Post.id == max_id).first()
    return latest_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_specific_to_id = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_specific_to_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found.")
    return post_specific_to_id


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post_data: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_specific_to_id = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_specific_to_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found.")
    if post_specific_to_id.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    db.query(models.Post).filter(models.Post.id == id).update(update_post_data.dict(), synchronize_session=False)
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_specific_to_id = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_specific_to_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found.")
    if post_specific_to_id.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    print(deleted_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
