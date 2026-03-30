from sqlalchemy import UUID, Table, Column, BigInteger, String, ForeignKey
from ..metadata import metadata


telegram_users_table = Table(
    "telegram_users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("telegram_id", BigInteger, unique=True, nullable=False),
    Column("username", String(255)),
    Column("last_name", String(255)),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
)
