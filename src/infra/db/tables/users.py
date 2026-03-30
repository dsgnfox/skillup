from sqlalchemy import (
    UUID,
    Boolean,
    Table,
    Column,
    String,
    DateTime,
)
from ..metadata import metadata


users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255)),
    Column("is_active", Boolean),
    Column("created_at", DateTime),
)
