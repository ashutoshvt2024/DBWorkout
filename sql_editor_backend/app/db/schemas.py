from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    course_instance_id: int

class UserOut(UserBase):
    user_id: int

    class Config:
        orm_mode = True