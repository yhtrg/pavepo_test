from fastapi import FastAPI, Depends, HTTPException, Response, Form, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
import uvicorn
from sqlalchemy import select

from config import config, security
from database import Base, UserModel
from schemas import UserSchema, UserGetSchema
from session_db import SessionDep, engine


app = FastAPI()

@app.post("/setup", tags=["Database"])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.post('/register', tags=["Authentication"])
async def register(user: UserSchema, session: SessionDep) -> UserSchema:
    result = await session.execute(
        select(UserModel).where(UserModel.username == user.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail={"message": "User already exists"})
    new_user = UserModel(
        username = user.username,
        password = user.password,
    )
    session.add(new_user)
    await session.commit()
    return user

@app.post('/login', tags=["Authentication"])
async def login(
    session: SessionDep,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    result = await session.execute(
        select(UserModel).where(UserModel.username == username)
    )
    user = result.scalars().first()

    if not user or user.password != password:
        raise HTTPException(401, detail={"message": "Bad credentials"})

    token = security.create_access_token(uid=username)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}

@app.get("/users", tags=["User"])
async def get_all_users(
    session: SessionDep
) -> list[UserGetSchema]:
    query = select(UserModel)
    result = await session.execute(query)
    users = result.scalars().all()
    return users

@app.get("/users/{id}", tags=["User"])
async def get_current_user(
    session: SessionDep,
    id: int,
) -> UserGetSchema:
    query = select(UserModel).where(UserModel.id == id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user

@app.get("/protected",
         dependencies=[Depends(security.access_token_required)],
         tags=["Authentication"])
def get_protected():
    return {"message": "Пользователь авторизирован"}

@app.post("/files", tags=["File"])
async def upload_file(uploaded_file: UploadFile, filename: str):
    file = uploaded_file.file
    with open(f"{filename}", "wb") as f:
        f.write(file.read())
    return {"message": "Файл успешно загружен"}

@app.get("/files/{filename}", tags=["File"])
async def get_file(filename: str):
    return FileResponse(filename)

def iterfile(filename: str):
    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk

@app.get("/files/streaming/{filename}", tags=["File"])
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfile(filename), media_type="music/mp3")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port="8000")