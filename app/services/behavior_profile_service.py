import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.db.models import BehaviorEvent, BehaviorProfile, User
from app.db.session import get_db
from app.config import settings

class BehaviorProfileService:
    """Service for managing user behavior profiles based on observable events."""

    @staticmethod
    def register_event(db: Session, user_id: str, event_type: str, details: Optional[Dict] = None):
        """Register a new behavior event for a user."""
        event = BehaviorEvent(
            user_id=uuid.UUID(user_id),
            event_type=event_type,
            details=json.dumps(details) if details else None
        )
        db.add(event)
        db.commit()

    @staticmethod
    def calculate_metrics(db: Session, user_id: str, days: int = 30) -> Dict:
        """Calculate behavior metrics from recent events (pure function)."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        events = db.query(BehaviorEvent).filter(
            BehaviorEvent.user_id == uuid.UUID(user_id),
            BehaviorEvent.timestamp >= cutoff
        ).all()

        total_messages = sum(1 for e in events if e.event_type == 'message_sent')
        negative_interactions = sum(1 for e in events if e.event_type in ['negative_interaction', 'warning_received'])
        floods = sum(1 for e in events if e.event_type == 'flood_detected')
        positive_interactions = sum(1 for e in events if e.event_type == 'positive_interaction')
        total_interactions = negative_interactions + positive_interactions

        # Engagement: messages per day
        active_days = max(1, (datetime.utcnow() - cutoff).days)
        messages_per_day = total_messages / active_days
        engagement_level = 'low' if messages_per_day < 5 else 'high' if messages_per_day > 20 else 'medium'

        # Conflict risk: negative / total interactions
        conflict_risk = negative_interactions / max(1, total_interactions)

        # Spam risk: floods / messages
        spam_risk = floods / max(1, total_messages)

        # Social integration: positive / total interactions
        social_integration = 'low' if positive_interactions / max(1, total_interactions) < 0.2 else 'high' if positive_interactions / max(1, total_interactions) > 0.5 else 'medium'

        return {
            'engagement_level': engagement_level,
            'conflict_risk': min(conflict_risk, 1.0),
            'spam_risk': min(spam_risk, 1.0),
            'social_integration': social_integration
        }

    @staticmethod
    def generate_recommendations(metrics: Dict) -> List[Dict]:
        """Generate recommendations based on metrics (pure function)."""
        recommendations = []
        factors = []

        if metrics['conflict_risk'] > settings.bps_conflict_risk_threshold:
            recommendations.append({
                'recommendation': 'warn_soft',
                'factors': ['high conflict_risk due to frequent negative interactions'],
                'metrics': {'conflict_risk': metrics['conflict_risk']}
            })
        if metrics['spam_risk'] > settings.bps_spam_risk_threshold:
            recommendations.append({
                'recommendation': 'limit_temporarily',
                'factors': ['high spam_risk due to detected floods'],
                'metrics': {'spam_risk': metrics['spam_risk']}
            })
        if metrics['engagement_level'] == 'high' and metrics['social_integration'] == 'low':
            recommendations.append({
                'recommendation': 'observe',
                'factors': ['high engagement but low social integration'],
                'metrics': {'engagement_level': metrics['engagement_level'], 'social_integration': metrics['social_integration']}
            })

        if not recommendations:
            recommendations.append({
                'recommendation': 'no_action',
                'factors': ['all metrics within normal ranges'],
                'metrics': metrics
            })

        return recommendations

    @staticmethod
    def recalculate_profile(db: Session, user_id: str):
        """Recalculate and update the behavior profile for a user."""
        metrics = BehaviorProfileService.calculate_metrics(db, user_id)
        recommendations = BehaviorProfileService.generate_recommendations(metrics)

        profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == uuid.UUID(user_id)).first()
        if not profile:
            profile = BehaviorProfile(user_id=uuid.UUID(user_id))
            db.add(profile)

        profile.engagement_level = metrics['engagement_level']
        profile.conflict_risk = metrics['conflict_risk']
        profile.spam_risk = metrics['spam_risk']
        profile.social_integration = metrics['social_integration']
        profile.recommendations = json.dumps(recommendations)
        profile.last_updated = datetime.utcnow()

        db.commit()

    @staticmethod
    def get_profile(db: Session, user_id: str) -> Optional[Dict]:
        """Get the current behavior profile for a user."""
        profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == uuid.UUID(user_id)).first()
        if profile:
            return {
                'engagement_level': profile.engagement_level,
                'conflict_risk': profile.conflict_risk,
                'spam_risk': profile.spam_risk,
                'social_integration': profile.social_integration,
                'last_updated': profile.last_updated.isoformat(),
                'recommendations': json.loads(profile.recommendations)
            }
        return None