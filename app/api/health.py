from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
import redis
from app.config import settings
import psutil
import time

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Endpoint to check the health of the service."""
    health_status = {
        "status": "ok",
        "service": "Hasbullita API",
        "checks": {}
    }
    
    # Database check
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = f"error: {str(e)}"
    
    # Redis check
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        health_status["checks"]["redis"] = "ok"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["redis"] = f"error: {str(e)}"
    
    if health_status["status"] != "ok":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status

@router.get("/metrics")
def metrics():
    """Basic metrics endpoint."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "uptime_seconds": time.time() - psutil.boot_time()
    }