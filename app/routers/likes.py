from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from ..database import get_db

router = APIRouter(prefix="/like", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like_type: schemas.Like, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_like = db.query(models.Post).filter(models.Post.id == like_type.post_id).first()
    if not post_to_like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post does not exist with id={like_type.post_id}")
    found_like = db.query(models.Likes).filter(models.Likes.post_id == like_type.post_id,
                                               models.Likes.user_id == current_user.id).first()
    if like_type.direction == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Post is already liked by current user whose user_id={current_user.id}")
        new_like = models.Likes(post_id=like_type.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Liked successfully."}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post is not liked by current user whose user_id={current_user.id}")
        db.query(models.Likes).filter(models.Likes.post_id == like_type.post_id,
                                      models.Likes.user_id == current_user.id).delete(synchronize_session=False)
        db.commit()
        return {"message": "Like removed successfully."}
