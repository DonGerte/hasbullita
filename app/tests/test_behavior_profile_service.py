import uuid
import pytest
from app.services.behavior_profile_service import BehaviorProfileService

def test_calculate_metrics_empty(db_session):
    """Test metrics calculation with no events."""
    test_user_id = str(uuid.uuid4())
    metrics = BehaviorProfileService.calculate_metrics(db_session, test_user_id)
    assert metrics["engagement_level"] == "low"
    assert metrics["conflict_risk"] == 0.0
    assert metrics["spam_risk"] == 0.0
    assert metrics["social_integration"] == "low"

def test_generate_recommendations_no_action(db_session):
    """Test recommendations for normal metrics."""
    metrics = {"engagement_level": "medium", "conflict_risk": 0.1, "spam_risk": 0.0, "social_integration": "medium"}
    recs = BehaviorProfileService.generate_recommendations(metrics)
    assert len(recs) == 1
    assert recs[0]["recommendation"] == "no_action"

def test_generate_recommendations_warn_soft(db_session):
    """Test recommendations for high conflict."""
    metrics = {"engagement_level": "medium", "conflict_risk": 0.6, "spam_risk": 0.0, "social_integration": "medium"}
    recs = BehaviorProfileService.generate_recommendations(metrics)
    assert any(r["recommendation"] == "warn_soft" for r in recs)