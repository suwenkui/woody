from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import models, schemas, crud, auth, database
from .database import engine
from sqlalchemy import text
import json

app = FastAPI(title="Woody API System")

# CORS Configuration
origins = [
    "http://localhost:3000", # Vue default port
    "http://localhost:5173", # Vite default port
    "*" # For development convenience
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (For simplicity in this demo, normally use migrations like Alembic)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    
    # Init system APIs
    async with database.SessionLocal() as session:
        system_apis = [
            {
                "name": "查询当前用户信息",
                "description": "获取当前登录用户的详细信息",
                "url": "/users/me",
                "method": "GET",
                "detail": json.dumps({
                    "params": [],
                    "response": {"username": "string", "id": "integer"}
                })
            },
            {
                "name": "查询用户总数",
                "description": "统计系统中注册用户的总数量",
                "url": "/users/count",
                "method": "GET",
                "detail": json.dumps({
                    "params": [],
                    "response": {"count": "integer"}
                })
            }
        ]
        
        for api_data in system_apis:
            db_api = await crud.get_api_by_name(session, api_data["name"])
            if not db_api:
                await crud.create_api(session, schemas.ApiInfoCreate(**api_data))

@app.get("/fix-db")
async def fix_db():
    async with engine.begin() as conn:
        await conn.execute(text('DROP TABLE IF EXISTS apis'))
        await conn.run_sync(models.Base.metadata.create_all)
    return {"message": "DB Fixed"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/auth/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")
    return await crud.create_user(db=db, user=user)

@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users/count")
async def read_users_count(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    count = await crud.get_user_count(db)
    return {"count": count}

@app.get("/apis", response_model=List[schemas.ApiInfo])
async def read_apis(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    apis = await crud.get_apis(db, skip=skip, limit=limit)
    return apis

@app.get("/apis/{api_id}", response_model=schemas.ApiInfo)
async def read_api(api_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_api = await crud.get_api(db, api_id=api_id)
    if db_api is None:
        raise HTTPException(status_code=404, detail="未找到该 API")
    return db_api

@app.post("/apis", response_model=schemas.ApiInfo)
async def create_api(api: schemas.ApiInfoCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return await crud.create_api(db=db, api=api)
