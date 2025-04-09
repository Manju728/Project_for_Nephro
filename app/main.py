from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.models import Schema

from app import crud, schemas, database, models
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/users/",response_model=schemas.UserInDB)
async def create_user(user: schemas.UserCreate,db: AsyncSession = Depends(database.get_db)):
    db_user = models.User(post_heading=user.post_heading, post_description=user.post_description)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.UserInDB])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_users(db, skip, limit)

@app.get("/users/{user_id}", response_model=schemas.UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserInDB)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(database.get_db)):
    updated_user = await crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    deleted_user = await crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}