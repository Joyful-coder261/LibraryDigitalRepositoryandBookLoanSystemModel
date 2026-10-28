"""Loans and reservations."""
from datetime import datetime
from sqlalchemy import (
    CheckConstraint, Computed, ForeignKey, ForeignKeyConstraint, Index,
    String, UniqueConstraint, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class Loan(Base):
    __tablename__ = "loans"
    __table_args__ = (
        UniqueConstraint("active_copy_id", name="uq_active_loan_copy"),
        CheckConstraint("loan_status IN ('active', 'overdue', 'returned', 'lost')", name="ck_loan_status"),
        CheckConstraint("due_at > borrowed_at", name="ck_loan_due_after_borrowed"),
        CheckConstraint("returned_at IS NULL OR returned_at >= borrowed_at", name="ck_loan_return_after_borrowed"),
        Index("ix_loans_issued_by", "issued_by"),
        Index("ix_loans_user_id", "user_id"),
        Index("ix_loans_copy_id", "copy_id"),
        Index("ix_loans_received_by", "received_by"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), nullable=False)
    copy_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("physical_copies.id"), nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime)
    loan_status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    issued_by: Mapped[int | None] = mapped_column(ID_TYPE, ForeignKey("users.id"))
    received_by: Mapped[int | None] = mapped_column(ID_TYPE, ForeignKey("users.id"))
    active_copy_id: Mapped[int | None] = mapped_column(
        ID_TYPE,
        Computed("CASE WHEN loan_status IN ('active', 'overdue') THEN copy_id ELSE NULL END", persisted=True),
    )


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fulfilled_copy_id", "resource_id"],
            ["physical_copies.id", "physical_copies.resource_id"],
            name="fk_reservation_fulfilled_copy_resource",
        ),
        ForeignKeyConstraint(["resource_id"], ["resources.id"], name="fk_reservation_resource"),
        CheckConstraint(
            "reservation_status IN ('pending', 'fulfilled', 'cancelled', 'expired')",
            name="ck_reservation_status",
        ),
        Index("ix_reservations_user_id", "user_id"),
        Index("ix_reservations_resource_id", "resource_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(ID_TYPE, nullable=False)
    reserved_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    reservation_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    fulfilled_copy_id: Mapped[int | None] = mapped_column(ID_TYPE)
