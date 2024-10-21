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

