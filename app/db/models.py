from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UUID, Float, Enum, Text
from sqlalchemy.sql import func
import uuid
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=False)
    reputation = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

class Group(Base):
    __tablename__ = "groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

class ModerationAction(Base):
    __tablename__ = "moderation_actions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    action = Column(String, nullable=False)  # ban, mute, etc.
    reason = Column(String)
    moderator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    timestamp = Column(DateTime, default=func.now())

class BehaviorEvent(Base):
    __tablename__ = "behavior_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_type = Column(String, nullable=False)  # e.g., 'message_sent', 'flood_detected'
    timestamp = Column(DateTime, default=func.now())
    details = Column(Text)  # JSON string for optional details

class BehaviorProfile(Base):
    __tablename__ = "behavior_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    engagement_level = Column(Enum('low', 'medium', 'high', name='engagement_enum'), default='medium')
    conflict_risk = Column(Float, default=0.0)
    spam_risk = Column(Float, default=0.0)
    social_integration = Column(Enum('low', 'medium', 'high', name='integration_enum'), default='medium')
    last_updated = Column(DateTime, default=func.now())
    recommendations = Column(Text)  # JSON string