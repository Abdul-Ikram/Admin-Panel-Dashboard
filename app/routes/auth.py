from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, LoginRequest, UserInfo, AuthResponse
from app.services.auth_service import AuthService
from app.database.db_config import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        return service.register_user(user_data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=AuthResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        return service.login_user(data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
