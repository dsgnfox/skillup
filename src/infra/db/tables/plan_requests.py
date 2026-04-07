from sqlalchemy import (
    UUID,
    Table,
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import ENUM

from src.domain.models.plan_request import (
    PlanRequestStatus,
)
from ..metadata import metadata


plan_requests_table = Table(
    "plan_requests",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "status",
        SQLEnum(PlanRequestStatus, name="status"),
        nullable=False,
    ),
    Column("request", String(), nullable=False),
    Column("plan_id", UUID(as_uuid=True), ForeignKey("plans.id")),
    Column("error_msg", String(500)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime),
)
