from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.roles import Role
from app.models.article import Article
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleResponse
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/search", response_model=list[ArticleResponse], summary="Search articles", description="Search articles by query, author_id or author_role with pagination.")
def search_articles(query: str | None = None, limit: int = 10, offset: int = 0, author_id: int | None = None, author_role: Role | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Article)
    if author_id:
        q = q.filter(Article.author_id==author_id)
    if author_role:
        q = q.join(User).filter(User.role==author_role)
    if query:
        q = q.filter(Article.title.ilike(f"%{query}%") | Article.content.ilike(f"%{query}%"))
    return q.offset(offset).limit(limit).all()

@router.get("/", response_model=list[ArticleResponse], summary="Get articles", description="Returns a paginated list of articles.")
def get_articles(limit: int = 10, offset: int = 0, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Article).offset(offset).limit(limit).all()

@router.get("/{article_id}", response_model=ArticleResponse, summary="Get article by ID", description="Returns a single article by its ID.")
def get_article(article_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    article = db.query(Article).filter(Article.id==article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article

@router.delete("/{article_id}", response_model=dict, summary="Delete article", description="Delete an article. Allowed for owner or admin.")
def delete_article(article_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    article = db.query(Article).filter(Article.id==article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this article")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted"}

@router.put("/{article_id}", response_model=ArticleResponse, summary="Update article", description="Update an existing article. Allowed for owner, admin, and editor.")
def update_article(article_id: int, updated_data: ArticleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    article = db.query(Article).filter(Article.id==article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if (article.author_id != user.id and user.role not in [Role.ADMIN, Role.EDITOR]):
        raise HTTPException(status_code=403, detail="You do not have permission to edit this article")

    article.title = updated_data.title
    article.content = updated_data.content
    db.commit()
    db.refresh(article)
    return article

@router.post("/", response_model=ArticleResponse, summary="Create article", description="Create a new article. The author is the currently authenticated user.")
def create_article(article: ArticleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_article = Article(
        title=article.title,
        content=article.content,
        author_id = user.id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
