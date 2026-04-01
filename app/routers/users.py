from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.roles import Role
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.core.dependencies import get_db
from app.core.permissions import require_role

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/search", response_model=list[UserResponse], summary="Search users", description="Search users by username or email (admin only).")
def search_users(query: str, limit: int = 10, offset: int = 0, db: Session = Depends(get_db), _: User = Depends(require_role([Role.ADMIN]))):
    return db.query(User).filter(User.username.ilike(f"%{query}%") | User.email.ilike(f"%{query}%")).offset(offset).limit(limit).all()

@router.get("/", response_model=list[UserResponse], summary="Get users", description="Returns list of all users (admin only).")
def get_users(limit: int = 10, offset: int = 0, db: Session = Depends(get_db), _: User = Depends(require_role([Role.ADMIN]))):
    return db.query(User).offset(offset).limit(limit).all()

@router.get("/{user_id}",  response_model=UserResponse, summary="Get user by ID", description="Returns a single user by ID (admin only).")
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role([Role.ADMIN]))):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=dict, summary="Delete user", description="Delete a user (admin only).")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role([Role.ADMIN]))):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/{user_id}", response_model=UserResponse, summary="Update user", description="Update user email and role (admin only).")
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_role([Role.ADMIN]))):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = updated_user.email
    user.role = updated_user.role
    db.commit()
    db.refresh(user)
    return user

