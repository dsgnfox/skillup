from sqlalchemy import Table, Column, UUID, String, Text, Integer, ForeignKey, DateTime
from ..metadata import metadata


steps_table = Table(
    "steps",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("content", Text, nullable=False),
    Column("status", Integer, nullable=False),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("plan_id", UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime),
)
