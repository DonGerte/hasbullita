from sqlalchemy.orm import Session
from app.db.models import ModerationAction
from app.services.reputation_service import adjust_reputation
from app.services.behavior_profile_service import BehaviorProfileService

def perform_moderation_action(db: Session, user_id: str, group_id: str, action: str, reason: str, moderator_id: str):
    """Perform a moderation action and adjust reputation automatically."""
    mod_action = ModerationAction(
        user_id=user_id,
        group_id=group_id,
        action=action,
        reason=reason,
        moderator_id=moderator_id
    )
    db.add(mod_action)
    db.commit()
    db.refresh(mod_action)
    
    # Automatic reputation adjustment
    if action == "ban":
        adjust_reputation(db, user_id, -5)  # Penalize banned user
        adjust_reputation(db, moderator_id, 1)  # Reward moderator
        BehaviorProfileService.register_event(db, user_id, 'warning_received', {'action': 'ban', 'reason': reason})
    elif action == "mute":
        adjust_reputation(db, user_id, -2)  # Penalize muted user
        adjust_reputation(db, moderator_id, 1)  # Reward moderator
        BehaviorProfileService.register_event(db, user_id, 'warning_received', {'action': 'mute', 'reason': reason})
    
    return mod_action