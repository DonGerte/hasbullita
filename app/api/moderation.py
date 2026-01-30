from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.moderation_service import perform_moderation_action
from app.config import settings

router = APIRouter()

@router.post("/ban")
def ban_user(user_id: str, group_id: str, reason: str, moderator_id: str, token: str, db: Session = Depends(get_db)):
    """Ban a user in a group."""
    if token != settings.core_secret:
        raise HTTPException(status_code=401, detail="Invalid token")
    action = perform_moderation_action(db, user_id, group_id, "ban", reason, moderator_id)
    return {"status": "banned", "action": action.id}

@router.post("/mute")
def mute_user(user_id: str, group_id: str, reason: str, moderator_id: str, token: str, db: Session = Depends(get_db)):
    """Mute a user in a group."""
    if token != settings.core_secret:
        raise HTTPException(status_code=401, detail="Invalid token")
    action = perform_moderation_action(db, user_id, group_id, "mute", reason, moderator_id)
    return {"status": "muted", "action": action.id}