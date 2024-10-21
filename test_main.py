import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base, Book, Review
from schemas import BookCreate, ReviewCreate
from main import create_book, get_books, get_book, update_book, delete_book, create_review, get_reviews
from fastapi import FastAPI, Depends

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="module")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    async with SessionLocal() as session:
        yield session
        await session.close()


@pytest.mark.anyio
async def test_create_book(db_session, setup_database):
    book_data = BookCreate(
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        year_published=2021
    )
    book = await create_book(db_session, book_data)
    assert book.title == "test book"
    assert book.author == "Test Author"

@pytest.mark.anyio
async def test_get_books(db_session, setup_database):
    books = await get_books(db_session)
    assert len(books) > 0

@pytest.mark.anyio
async def test_get_book(db_session, setup_database):
    book = await get_book(db_session, 1)
    assert book is not None
    assert book.title == "test book"

@pytest.mark.anyio
async def test_update_book(db_session, setup_database):
    update_data = {"title": "Updated Book"}
    book = await update_book(db_session, 1, update_data)
    assert book.title == "Updated Book"

@pytest.mark.anyio
async def test_delete_book(db_session, setup_database):
    book = await delete_book(db_session, 1)
    assert book is not None

@pytest.mark.anyio
async def test_create_review(db_session, setup_database):
    review_data = ReviewCreate(
        user_id=1,
        review_text="Great book!",
        rating=5
    )
    review = await create_review(db_session, 1, review_data)
    assert review.review_text == "Great book!"
    assert review.rating == 5

@pytest.mark.anyio
async def test_get_reviews(db_session, setup_database):
    reviews = await get_reviews(db_session, 1)
    assert len(reviews) > 0
