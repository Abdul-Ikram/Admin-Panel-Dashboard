from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db_config import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
def create_dashboard(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = DashboardService(db)
    return service.create_random_dashboard()


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = DashboardService(db)
    data = service.get_latest_dashboard()
    if not data:
        return {"message": "No dashboard data available. Please POST first."}
    return data
