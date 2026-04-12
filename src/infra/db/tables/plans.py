from sqlalchemy import (
    UUID,
    Integer,
    Table,
    Column,
    String,
    ForeignKey,
)

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
        Integer,
        nullable=False,
    ),
)
