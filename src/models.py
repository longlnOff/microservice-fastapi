from pydantic import (  BaseModel,
                        Field
                     )

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., gt=0, lt=2023)
