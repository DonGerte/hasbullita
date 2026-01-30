from app.db.base import Base
from app.db.session import engine

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)