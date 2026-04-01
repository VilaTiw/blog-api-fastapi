from pydantic import BaseModel, Field

class ArticleCreate(BaseModel):
    title: str = Field(..., example="Interesting title")
    content: str = Field(..., example="Interesting content")

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True
        
