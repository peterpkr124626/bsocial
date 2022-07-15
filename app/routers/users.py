from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, utils, models
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(new_user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(new_user_data.password)
    new_user_data.password = hashed_password
    new_user = models.User(**new_user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user_specific_to_id = db.query(models.User).filter(models.User.id == id).first()
    if not user_specific_to_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={id} does not exist.")
    return user_specific_to_id
