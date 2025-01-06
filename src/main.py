from fastapi import (
                        FastAPI,
                        Depends,
                        HTTPException
                    )
from src.database import (
                            SessionLocal,
                            User
                        )
from sqlalchemy.orm import Session
import src.authors as authors
import src.books as books
import src.models as models
from pydantic import (
                        BaseModel,
                        EmailStr
                    )



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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


class UserCreate(BaseModel):
    name: str
    email: EmailStr

@app.post("/user")
def add_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.post("/user/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if user_to_update:
        user_to_update.name = user.name
        user_to_update.email = user.email
        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.delete("/user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")