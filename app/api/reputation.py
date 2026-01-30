from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.db.session import get_db
from app.db.models import User, ModerationAction
from app.services.behavior_profile_service import BehaviorProfileService
from app.config import settings

router = APIRouter()

@router.get("/user/{user_id}")
def get_reputation(user_id: str, db: Session = Depends(get_db)):
    """Get user reputation."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"reputation": user.reputation}

@router.post("/user/{user_id}")
def update_reputation(user_id: str, delta: int, token: str, db: Session = Depends(get_db)):
    """Update user reputation."""
    if token != settings.core_secret:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.reputation += delta
    db.commit()
    return {"new_reputation": user.reputation}

@router.get("/user/{user_id}/history")
def get_reputation_history(user_id: str, db: Session = Depends(get_db)):
    """Get reputation change history for user."""
    actions_as_user = db.query(ModerationAction).filter(ModerationAction.user_id == user_id).all()
    actions_as_moderator = db.query(ModerationAction).filter(ModerationAction.moderator_id == user_id).all()
    
    history = []
    for action in actions_as_user:
        delta = -5 if action.action == "ban" else -2 if action.action == "mute" else 0
        history.append({
            "timestamp": action.timestamp,
            "action": action.action,
            "reason": action.reason,
            "delta": delta,
            "role": "target"
        })
    for action in actions_as_moderator:
        delta = 1 if action.action in ["ban", "mute"] else 0
        history.append({
            "timestamp": action.timestamp,
            "action": action.action,
            "reason": action.reason,
            "delta": delta,
            "role": "moderator"
        })
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    return {"history": history}

@router.get("/user/{user_id}/behavior")
def get_behavior_profile(user_id: str, db: Session = Depends(get_db)):
    """Get the behavior profile for a user."""
    profile = BehaviorProfileService.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Behavior profile not found")
    return profile

@router.post("/user/{user_id}/recalculate")
def recalculate_behavior_profile(user_id: str, token: str, db: Session = Depends(get_db)):
    """Recalculate the behavior profile for a user."""
    if token != settings.core_secret:
        raise HTTPException(status_code=401, detail="Invalid token")
    BehaviorProfileService.recalculate_profile(db, user_id)
    return {"status": "recalculated"}

@router.post("/register_event")
def register_behavior_event(user_id: str, event_type: str, details: Optional[Dict] = None, token: str = None, db: Session = Depends(get_db)):
    """Register a behavior event for BPS."""
    if token != settings.core_secret:
        raise HTTPException(status_code=401, detail="Invalid token")
    BehaviorProfileService.register_event(db, user_id, event_type, details)
    return {"status": "registered"}