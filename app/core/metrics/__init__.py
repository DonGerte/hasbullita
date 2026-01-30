import logging
from datetime import datetime
from app.storage.models import Metric, User, Interaction
from sqlalchemy.orm import Session
from app.core.config import config

logger = logging.getLogger(__name__)

def log_interaction(user_id: int, interaction_type: str, content_length: int, is_initiative: int, db: Session):
    """Log an interaction."""
    interaction = Interaction(
        user_id=user_id,
        interaction_type=interaction_type,
        content_length=content_length,
        is_initiative=is_initiative
    )
    db.add(interaction)
    db.commit()

    if config.ENABLE_EXTENDED_LOGGING:
        logger.info(f"Interaction logged: user {user_id}, type {interaction_type}")

def log_error(error: str):
    """Log an error."""
    logger.error(f"Bot error: {error}")

def update_daily_metrics(db: Session):
    """Update daily metrics."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    metric = db.query(Metric).filter(Metric.date == today).first()
    if not metric:
        metric = Metric(date=today)
        db.add(metric)

    # Calculate metrics
    start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    users_today = db.query(User).filter(User.first_seen >= start_of_day).count()
    interactions_today = db.query(Interaction).filter(Interaction.timestamp >= start_of_day).count()

    # Simple retention calculation (placeholder)
    metric.unique_users = users_today
    metric.total_interactions = interactions_today
    # TODO: Implement proper retention calculation

    db.commit()

    if config.ENABLE_EXTENDED_LOGGING:
        logger.info(f"Metrics updated for {today}")