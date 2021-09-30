from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.security import oauth2
from sqlalchemy.orm import Session, session
from . import models
from passlib.context import CryptContext
from fastapi import Depends, status
from datetime import datetime, timedelta
from .main import SECRET_KEY, ALGORITHM, oauth2_scheme
from jose import jwt, JWTError
from .database import get_db

def get_user_by_username(username: str, db: Session = Depends(get_db) ) -> models.User:
    return db.query(models.User).filter(models.User.username.lower() == username.lower()).first()

def get_user_by_email(email: str, db: Session = Depends(get_db)) -> models.User:
   return db.query(models.User).filter(models.User.email.lower() == email.lower()).first()

def get_user(db: Session = Depends(get_db), email: Optional[str] = None, username: Optional[str] = None):
    if email:
        return get_user_by_email(db, email)
    elif username:
        return get_user_by_username(db, username)
    else:
        return False
def verify_password(plain_password: str, hashed_password: str, context: CryptContext):
    return context.verify(plain_password, hashed_password)

def hash_plain_text_password(password: str, context: CryptContext):
    return context.hash(password)

def authenticate_user(password:str, db: Session = Depends(get_db), user: models.User = Depends()):
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15) 
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        email: str = payload.get("email")
        if username and email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user( username=username)
    if user is None:
        raise credentials_exception
    return user 
    