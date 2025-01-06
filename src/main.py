from fastapi import FastAPI
import src.authors as authors
import src.books as books
import src.models as models
from pydantic import BaseModel


app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)


@app.post("/book")
async def create_book(book: models.Book):
    return book

class BookResponse(BaseModel):
    title: str
    author: str

@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {
            "id": 1,
            "title": "Book 1",
            "author": "Author 1"
        },
        {
            "id": 2,
            "title": "Book 2",
            "author": "Author 2"
        }
    ]
