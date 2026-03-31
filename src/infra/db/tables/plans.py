from sqlalchemy import (
    UUID,
    Table,
    Column,
    String,
    ForeignKey,
    Enum as SQLEnum,
)

from src.domain.models.plan import PlanStatus
from ..metadata import metadata


plans_table = Table(
    "plans",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "status",
        SQLEnum(PlanStatus, name="status"),
        nullable=False,
        default=PlanStatus.DRAFT,
    ),
)
