from typing import Optional
from app.storage.models import UserProfile, Interaction
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class ProfileType:
    EXPLORADOR = "explorador"  # Low frequency, high initiative
    OCASIONAL = "ocasional"   # Medium frequency, balanced
    REACTIVO = "reactivo"     # High frequency, low initiative
    INTENSIVO = "intensivo"   # High frequency, high initiative

def calculate_profile(user_id: int, db: Session) -> str:
    """Calculate user profile based on interactions."""
    # Get interactions from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    interactions = db.query(Interaction).filter(
        Interaction.user_id == user_id,
        Interaction.timestamp >= thirty_days_ago
    ).all()

    if not interactions:
        return ProfileType.EXPLORADOR

    total_days = 30
    total_interactions = len(interactions)
    usage_frequency = total_interactions / total_days

    avg_length = sum(i.content_length for i in interactions) / total_interactions if total_interactions > 0 else 0
    initiative_count = sum(i.is_initiative for i in interactions)
    initiative_level = initiative_count / total_interactions if total_interactions > 0 else 0

    # Simple classification
    if usage_frequency < 0.5:
        return ProfileType.EXPLORADOR
    elif usage_frequency < 2.0:
        if initiative_level > 0.6:
            return ProfileType.OCASIONAL
        else:
            return ProfileType.REACTIVO
    else:
        if initiative_level > 0.7:
            return ProfileType.INTENSIVO
        else:
            return ProfileType.REACTIVO

def get_or_create_profile(user_id: int, db: Session) -> UserProfile:
    """Get existing profile or create new one."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile_type = calculate_profile(user_id, db)
        profile = UserProfile(
            user_id=user_id,
            profile_type=profile_type,
            usage_frequency=0.0,
            avg_interaction_length=0.0,
            initiative_level=0.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def update_profile(user_id: int, db: Session):
    """Update profile with latest data."""
    profile = get_or_create_profile(user_id, db)
    profile_type = calculate_profile(user_id, db)
    profile.profile_type = profile_type
    # Update other fields if needed
    db.commit()