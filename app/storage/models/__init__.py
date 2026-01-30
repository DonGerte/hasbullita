from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    chat_type = Column(String, nullable=False)  # 'private' or 'group'
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    profile_type = Column(String, nullable=False)  # 'explorador', 'ocasional', 'reactivo', 'intensivo'
    usage_frequency = Column(Float, default=0.0)  # interactions per day
    avg_interaction_length = Column(Float, default=0.0)  # average message length
    initiative_level = Column(Float, default=0.0)  # 0-1, how often user initiates
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(String, nullable=False)  # 'command', 'short_text', 'long_text'
    content_length = Column(Integer, default=0)
    is_initiative = Column(Integer, default=0)  # 1 if user initiated, 0 if response

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    unique_users = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_interactions = Column(Integer, default=0)
    day1_retention = Column(Float, default=0.0)
    day7_retention = Column(Float, default=0.0)
    errors_count = Column(Integer, default=0)