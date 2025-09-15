import random
from sqlalchemy.orm import Session
from app.models.dashboard import Dashboard
from app.schemas.dashboard import Stats, AgentStats, CallStats, DashboardResponse


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def create_random_dashboard(self) -> DashboardResponse:
        """Insert random dashboard data into DB"""

        tool_sync_cost = random.uniform(1000, 5000)
        total_calls = random.randint(5000, 15000)
        total_users = random.randint(1000, 5000)
        total_revenue = random.uniform(2000, 10000)

        total_agents = random.randint(500, 2000)
        active_agents = random.randint(100, total_agents)
        inactive_agents = total_agents - active_agents

        success_calls_today = random.randint(500, 2000)
        failed_calls_today = random.randint(50, 500)

        dashboard = Dashboard(
            tool_sync_cost=tool_sync_cost,
            total_calls=total_calls,
            total_users=total_users,
            total_revenue=total_revenue,
            total_agents=total_agents,
            active_agents=active_agents,
            inactive_agents=inactive_agents,
            success_calls_today=success_calls_today,
            failed_calls_today=failed_calls_today,
        )

        self.db.add(dashboard)
        self.db.commit()
        self.db.refresh(dashboard)

        return self._map_to_response(dashboard)

    def get_latest_dashboard(self) -> DashboardResponse:
        """Fetch the most recent dashboard record"""
        dashboard = (
            self.db.query(Dashboard)
            .order_by(Dashboard.created_at.desc())
            .first()
        )
        if not dashboard:
            return None
        return self._map_to_response(dashboard)

    def _map_to_response(self, dashboard: Dashboard) -> DashboardResponse:
        return DashboardResponse(
            stats=Stats(
                tool_sync_cost=dashboard.tool_sync_cost,
                total_calls=dashboard.total_calls,
                total_users=dashboard.total_users,
                total_revenue=dashboard.total_revenue,
            ),
            agent_stats=AgentStats(
                total_agents=dashboard.total_agents,
                active_agents=dashboard.active_agents,
                inactive_agents=dashboard.inactive_agents,
            ),
            call_stats=CallStats(
                success_calls_today=dashboard.success_calls_today,
                failed_calls_today=dashboard.failed_calls_today,
            ),
        )
