from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database.db_config import Base
import uuid


class Dashboard(Base):
    __tablename__ = "dashboard"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tool_sync_cost = Column(Float, nullable=False)
    total_calls = Column(Integer, nullable=False)
    total_users = Column(Integer, nullable=False)
    total_revenue = Column(Float, nullable=False)

    total_agents = Column(Integer, nullable=False)
    active_agents = Column(Integer, nullable=False)
    inactive_agents = Column(Integer, nullable=False)

    success_calls_today = Column(Integer, nullable=False)
    failed_calls_today = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
