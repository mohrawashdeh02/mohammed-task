from pydantic import BaseModel
from datetime import datetime

# -------- Category --------
class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------- Post --------
class PostCreate(BaseModel):
    category_id: int
    title: str
    body: str

class PostOut(BaseModel):
    id: int
    category_id: int
    title: str
    body: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------- Comment --------
class CommentCreate(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    body: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

