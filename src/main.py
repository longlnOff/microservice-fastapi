from fastapi import FastAPI
import src.authors as authors
import src.books as books

app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)



