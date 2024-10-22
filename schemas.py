from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int

class ReviewCreate(BaseModel):
    user_id: int
    review_text: str
    rating: int

class Token(BaseModel):
    access_token: str
    token_type: str

