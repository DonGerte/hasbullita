from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/verify")
def verify_token(token: str):
    """Verify the shared secret token."""
    from app.config import settings
    if token == settings.core_secret:
        return {"verified": True}
    raise HTTPException(status_code=401, detail="Invalid token")