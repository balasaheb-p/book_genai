from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

async def create_book_content(book_topic):
    prompt = f"""
    You are a book writer AI, 
    Based on user given book topic create a book in 400 words.
    write only book content, do not provide additional details over the content.
    
    book_topic: {book_topic}
    
    book_content:
    """
    print(f"Generating book content for tile: {book_topic}")
    result = llm.invoke(prompt)
    print(f"Generated book content for tile: {book_topic}")
    return result

async def create_book_summary(book_content):
    prompt = f"""
    You are a book writer AI, 
    Based on given book content create abook summary in 40 words.
    write only book summary, do not provide additional details over the summary.
    
    book_content: {book_content}

    book_summary:
    """
    print("Generating book summary.")
    summary = llm.invoke(prompt)
    print("Generated book summary.")
    return summary

async def create_review_summary(book_title, book_reviews):
    prompt = f"""
    You are a book writer AI, 
    Based on given book content create a book reviews summary in 40 words.
    write only review summary, do not provide additional details over the summary.

    book_title: {book_title}
    book_review: {book_reviews}
    
    reviews_summary:
    """
    print("Generating reviews summary.")
    summary = llm.invoke(prompt)
    print("Generated reviews summary.")
    return summary


async def get_book_recommendation(book_titles_and_its_review, books_available_to_read):
    prompt = f"""
    You are a book writer AI, 
    Based on given reviewed book titles and its reviews recommend book from from the available book to read.
    write only book name, do not provide additional details over the summary.

    book titles and its review: {book_titles_and_its_review}
    books available to read: {books_available_to_read}

    book recommendation:
    """
    print("Generating book recommendation.")
    summary = llm.invoke(prompt)
    print("Generated book recommendation.")
    return summary

if __name__ == '__main__':
    book_topic = "Tree"
    book_content = create_book_content(book_topic)
    print("*"*50)
    print(book_content)

    book_summary = create_book_summary(book_content)
    print("*" * 50)
    print(book_summary)
    
    book_reviews = ["Book is awesome", "it would be better to have info nature saving and global warming", "overall book content is good"]
    reviews_summary = create_review_summary(book_topic, book_reviews)
    print("*" * 50)
    print(reviews_summary)
    