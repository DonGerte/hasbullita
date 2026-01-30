import redis
from app.config import settings
from app.services.behavior_profile_service import BehaviorProfileService
from sqlalchemy.orm import Session

redis_client = redis.from_url(settings.redis_url)

def check_rate_limit(key: str, limit: int = 10, window: int = 60) -> bool:
    """Check if the given key is within rate limit. Returns True if allowed, False if exceeded."""
    redis_key = f"rate_limit:{key}"
    count = redis_client.incr(redis_key)
    if count == 1:
        redis_client.expire(redis_key, window)
    return count <= limit

def register_flood_event(db: Session, user_id: str):
    """Register a flood event and trigger profile recalculation."""
    BehaviorProfileService.register_event(db, user_id, 'flood_detected')
    # TODO: Consider batch recalculation instead of immediate for performance