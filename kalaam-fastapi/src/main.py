from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import models
from . import services
from .database import engine, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

pwd_context = CryptContext(schemes=['bcrypt'], depracated='auto')

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = '6adef5d03537d79978ac0e1d5fac2083c277008c3bebabe3a17b6c714d61bad7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30



@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/test/")
async def test(token:str = Depends(oauth2_scheme)):
    return {'token', token}

@app.post('/login/{method}')
async def login(method: str, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), ):
    user = services.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"username": user.username, "email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

