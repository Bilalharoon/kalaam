from fastapi import Depends, FastAPI, HTTPException, status

import models
import services
import schemas
from database import engine, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, oauth2

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'] )

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = services.oauth2_scheme


@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/test/")
async def test(token:str = Depends(oauth2_scheme)):
    return {'token', token}

@app.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(form_data.username, form_data.password, db=db, ctx=pwd_context)
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

@app.post('/signup/')
async def signup(user: schemas.UserCreate, db:Session = Depends(get_db)):

    return await services.create_user(user, pwd_context, db)
    