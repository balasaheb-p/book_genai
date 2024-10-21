from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, Review
from schemas import BookCreate , ReviewCreate
from ollama_call import create_book_content, create_book_summary, create_review_summary, get_book_recommendation

async def create_book(db: AsyncSession, book: BookCreate):
    book_exist = await db.execute(select(Book).filter(Book.title == book.title))
    book_record = book_exist.scalars().first()
    if book_record:
        return "book is already exist, please try to create a new book with different title..!"

    # Call genAI LLama3 model to generate book content and summary
    book_content = await create_book_content(book.title)
    book_summary = await create_book_summary(book_content)

    book_data= Book(title = book.title.lower(),
                    author = book.author,
                    genre = book.genre,
                    year_published = book.year_published,
                    book_content = book_content,
                    summary = book_summary)

    db.add(book_data)
    await db.commit()
    await db.refresh(book_data)
    return book_data

async def get_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    return result.scalar_one_or_none()

async def update_book(db: AsyncSession, book_id: int, book_data: dict):
    book = await get_book(db, book_id)
    if book:
        for key, value in book_data.items():
            setattr(book, key, value)
        await db.commit()
        await db.refresh(book)
    return book

async def delete_book(db: AsyncSession, book_id: int):
    book = await get_book(db, book_id)
    if book:
        await db.delete(book)
        await db.commit()
    return book

async def create_review(db: AsyncSession, book_id, review: ReviewCreate):
    review_data = Review(book_id = book_id,
                         user_id = review.user_id,
                         review_text = review.review_text,
                         rating = review.rating)
    db.add(review_data)
    await db.commit()
    await db.refresh(review_data)
    return review_data

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    return result.scalars().all()

async def generate_recommendations(db: AsyncSession, user_id: int):

    # get all books & reviews for read books by user
    # Get all books not read by user
    # pass these two lists to prompt to get next book recommendation


    reviews = await db.execute(select(Review).filter(Review.user_id == user_id))
    reviews = reviews.scalars().all()

    book_and_reviews = {}
    for review in reviews:
        book_id = review.book_id
        review = review.review_text

        book_title = await db.execute(select(Book.title).filter(Book.id == book_id))
        book_title = book_title.scalars().first()

        if book_and_reviews.get(book_title):
            book_and_reviews[book_title].append(review)
        else:
            book_and_reviews[book_title] = [review]

    print("book_title_and_reviews>>>>>>>>>", book_and_reviews)

    reviewed_books = set(book_and_reviews.keys())

    available_books = await db.execute(select(Book.title))
    available_books = set(available_books.scalars().all())

    books_for_recommendation = available_books.difference(reviewed_books)

    print("books_for_recommendation>>>>>>>>>", books_for_recommendation)

    recommended_book = await get_book_recommendation(book_and_reviews, books_for_recommendation)

    return recommended_book

async def generate_summary(db: AsyncSession, book_title: str):

    book_details = await db.execute(select(Book).filter(Book.title == book_title))
    book_details = book_details.scalars().first()
    book_content = book_details.book_content

    book_summary = await create_book_summary(book_content)
    print("book_summary>>>>>>>>", book_summary)

    review_details = await db.execute(select(Review.review_text).filter(Review.book_id == book_details.id))
    review_details = review_details.scalars().all()

    reviews_summary = await create_review_summary(book_details.title, review_details)
    print("reviews_summary>>>>>>", reviews_summary)
    
    return {
        "book_summary": book_summary,
        "reviews_summary": reviews_summary
    }

if __name__ == '__main__':
    pass