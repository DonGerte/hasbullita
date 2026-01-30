from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Group

router = APIRouter()

@router.post("/")
def create_group(name: str, telegram_id: int, db: Session = Depends(get_db)):
    """Create a new group."""
    group = Group(name=name, telegram_id=telegram_id)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.get("/{group_id}")
def get_group(group_id: str, db: Session = Depends(get_db)):
    """Get a group by ID."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/")
def list_groups(db: Session = Depends(get_db)):
    """List all groups."""
    return db.query(Group).all()