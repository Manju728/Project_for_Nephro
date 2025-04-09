from pydantic import BaseModel

class UserBase(BaseModel):
    post_heading: str
    post_description: str

class UserCreate(UserBase):
    post_heading: str
    post_description: str

class UserInDB(UserBase):
    id: int

class UserUpdate(UserBase):
    post_heading: str
    post_description: str

    class Config:
        orm_mode = True
