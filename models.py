from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    year_published = Column(Integer)
    book_content = Column(Text, default='')
    summary = Column(Text, default='')
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey(Book.id))
    user_id = Column(Integer)
    review_text = Column(Text)
    rating = Column(Integer)
    book = relationship("Book", back_populates="reviews")
