from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.security import oauth2
from sqlalchemy.orm import Session, query, session
from sqlalchemy.sql.expression import false
import models
import schemas
from passlib.context import CryptContext
from fastapi import Depends, status
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

SECRET_KEY = '6adef5d03537d79978ac0e1d5fac2083c277008c3bebabe3a17b6c714d61bad7'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_user_by_username(username: str, db: Session ) -> schemas.User:
    return db.query(models.User).filter(models.User.username.lower() == username.lower()).first()

async def get_user_by_email(email: str, db: Session = Depends(get_db)) -> schemas.User:
   return db.query(models.User).filter(models.User.email.lower() == email.lower()).first()

async def get_user(db: Session = Depends(get_db), email: Optional[str] = None, username: Optional[str] = None):
    if email:
        return await get_user_by_email(db, email)
    elif username:
        return await get_user_by_username(db, username)
    else:
        return False
def verify_password(plain_password: str, hashed_password: str, context: CryptContext):
    return context.verify(plain_password, hashed_password)

def hash_plain_text_password(password: str, context: CryptContext):
    return context.hash(password)

def authenticate_user(username: str, password:str, db: Session, ctx: CryptContext):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password, ctx):
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
    
async def create_user(user: schemas.UserCreate, ctx:CryptContext, db: Session = Depends(get_db)):
    


    userdb= models.User(username=user.username, email=user.email, hashed_password=hash_plain_text_password(user.password, ctx))
    db.add(userdb)
    db.commit()
    db.refresh(userdb)
    db.commit()
    return userdb
