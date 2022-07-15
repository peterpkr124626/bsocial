from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(access_token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not able to validate credentials.",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(access_token, credentials_exception)
    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    return current_user


def verify_access_token(access_token: str, credentials_exception):
    try:
        payload_data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload_data.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def create_access_token(payload_data: dict):
    to_encode = payload_data.copy()
    expiring_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiring_time})
    encoded_jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt_token


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
