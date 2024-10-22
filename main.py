from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from database import get_db, engine, Base
from crud import create_book, get_books, get_book, update_book, delete_book, create_review, get_reviews, generate_summary, generate_recommendations
from schemas import BookCreate, ReviewCreate, Token
import jwt

SECRET_KEY = "ZPqJGvzoLYHIFxGLvqlT6gzdCEf8LTtCbu5zQb1lLmo"  # Replace with a securely generated key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Fake user database for demonstration purposes
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "secretpassword"  # In practice, we will store hashed passwords
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or form_data.password != user['password']:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/books")
async def add_book(book_data: BookCreate, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    return await create_book(db, book_data)

@app.get("/books")
async def read_books(db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    return await get_books(db)

@app.get("/books/{book_id}")
async def read_book(book_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    book = await get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
async def update_book_info(book_id: int, book_data: dict, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    book = await update_book(db, book_id, book_data)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
async def delete_book_info(book_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    book = await delete_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}

@app.post("/books/{book_id}/reviews")
async def add_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    return await create_review(db, book_id, review)

@app.get("/books/{book_id}/reviews")
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    return await get_reviews(db, book_id)

@app.get("/recommendations")
async def get_recommendations(user_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    recommendation = await generate_recommendations(db, user_id)
    return {"message": recommendation}

@app.post("/generate-summary")
async def generate_summary_endpoint(book_title: str, db: AsyncSession = Depends(get_db), token: str = Depends(security)):
    token_value = token.credentials
    verify_token(token_value)
    result = await generate_summary(db, book_title)
    return {"summary": result}

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
