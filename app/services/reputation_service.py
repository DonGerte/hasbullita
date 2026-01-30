from sqlalchemy.orm import Session
from app.db.models import User

def adjust_reputation(db: Session, user_id: str, delta: int):
    """Adjust user reputation."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.reputation += delta
        db.commit()
        return user.reputation
    return None