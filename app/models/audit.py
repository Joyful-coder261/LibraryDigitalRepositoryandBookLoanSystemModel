"""Audit trail and authentication event records."""
from datetime import datetime
from sqlalchemy import ForeignKey, Index, JSON, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_actor_user_id", "actor_user_id"),)
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    actor_user_id: Mapped[int | None] = mapped_column(ID_TYPE, ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(100))
    old_values: Mapped[dict | None] = mapped_column(JSON)
    new_values: Mapped[dict | None] = mapped_column(JSON)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())


class LoginEvent(Base):
    __tablename__ = "login_events"
    __table_args__ = (Index("ix_login_events_user_id", "user_id"),)
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ID_TYPE, ForeignKey("users.id"))
    attempted_identifier: Mapped[str | None] = mapped_column(String(255))
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
