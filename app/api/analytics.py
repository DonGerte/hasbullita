from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User, Group, ModerationAction

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get basic statistics."""
    user_count = db.query(User).count()
    group_count = db.query(Group).count()
    action_count = db.query(ModerationAction).count()
    return {"users": user_count, "groups": group_count, "moderation_actions": action_count}