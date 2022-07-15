from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def log_in(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_specific_to_email = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user_specific_to_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials provided.")
    if not utils.verify(user_credentials.password, user_specific_to_email.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials provided.")
    access_token = oauth2.create_access_token(payload_data={"user_id": user_specific_to_email.id})
    return {"access_token": access_token, "token_type": "bearer"}
