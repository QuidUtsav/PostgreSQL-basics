from pydantic import BaseModel, EmailStr

class CreateAuthor(BaseModel):
    name: str
    email:EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class CreatePost(BaseModel):
    title:str
    content:str
    author_id: int
    
class CreateComment(BaseModel):
    content:str
    post_id:int
    user_id:int