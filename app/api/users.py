from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User

router = APIRouter()

@router.post("/")
def create_user(username: str, telegram_id: int, db: Session = Depends(get_db)):
    """Create a new user."""
    user = User(username=username, telegram_id=telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/by_telegram/{telegram_id}")
def get_user_by_telegram(telegram_id: int, db: Session = Depends(get_db)):
    """Get a user by Telegram ID."""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    """List all users."""
    return db.query(User).all()