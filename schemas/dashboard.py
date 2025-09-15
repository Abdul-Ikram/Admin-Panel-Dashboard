from pydantic import BaseModel
from typing import List


class Stats(BaseModel):
    tool_sync_cost: float
    total_calls: int
    total_users: int
    total_revenue: float


class AgentStats(BaseModel):
    total_agents: int
    active_agents: int
    inactive_agents: int


class CallStats(BaseModel):
    success_calls_today: int
    failed_calls_today: int


class DashboardResponse(BaseModel):
    stats: Stats
    agent_stats: AgentStats
    call_stats: CallStats

    class Config:
        from_attributes = True
