from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine, Base
# from models import Book, Review
from crud import create_book, get_books, get_book, update_book, delete_book, create_review, get_reviews, generate_summary, generate_recommendations
from schemas import BookCreate, ReviewCreate


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/books")
async def add_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book(db, book_data)

@app.get("/books")
async def read_books(db: AsyncSession = Depends(get_db)):
    return await get_books(db)

@app.get("/books/{book_id}")
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
async def update_book_info(book_id: int, book_data: dict, db: AsyncSession = Depends(get_db)):
    book = await update_book(db, book_id, book_data)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
async def delete_book_info(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await delete_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}

@app.post("/books/{book_id}/reviews")
async def add_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await create_review(db, book_id, review)

@app.get("/books/{book_id}/reviews")
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    return await get_reviews(db, book_id)

@app.get("/recommendations")
async def get_recommendations(user_id: int, db: AsyncSession = Depends(get_db)):
    # Implement recommendation logic here
    recommendation = await generate_recommendations(db, user_id)

    return {"message": recommendation}

@app.post("/generate-summary")
async def generate_summary_endpoint(book_title: str, db: AsyncSession = Depends(get_db)):
    result = await generate_summary(db, book_title)
    # return {"book_summary": summary, "reviews_summary": reviews}
    return {"summary": result}

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)