from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserGetSchema(BaseModel):
    id: int
    username: str
    password: str