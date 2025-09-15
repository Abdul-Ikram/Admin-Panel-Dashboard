from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models.admin import Admin
from app.schemas.auth import RegisterRequest, LoginRequest, UserInfo, AuthResponse
from app.utils.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, user_data: RegisterRequest) -> UserInfo:
        # Check if email already exists
        existing_user = self.db.query(Admin).filter(Admin.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        new_user = Admin(
            name=user_data.name,
            email=user_data.email,
            password_hash=self.hash_password(user_data.password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return UserInfo.from_orm(new_user)

    def login_user(self, data: LoginRequest) -> AuthResponse:
        user = self.db.query(Admin).filter(Admin.email == data.email).first()
        if not user or not self.verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token({"sub": str(user.id)})

        return AuthResponse(
            access_token=token,
            user=UserInfo.from_orm(user)
        )
