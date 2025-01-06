from fastapi import APIRouter

router = APIRouter()



@router.get("/books/{book_id}")
async def get_book(book_id: int):
    return {"book_id": book_id}

@router.get("/books")
async def read_books(year: int | None = None):
    if year:
        return {"year": year,
                "books": ["Book 1", "Book 2"]}
    else:
        return {"books": ["All Books"]}
