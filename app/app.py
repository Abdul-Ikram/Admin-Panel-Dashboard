from fastapi import FastAPI
from app.database.db_config import Base, engine
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router

# Create all tables if they don't exist (good for dev, use Alembic for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin Auth API")

# Register routers
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "Welcome to Admin Auth API 🚀"}
