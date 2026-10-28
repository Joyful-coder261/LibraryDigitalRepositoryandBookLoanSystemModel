"""Physical book copies and their circulation state."""
from datetime import date
from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class PhysicalCopy(Base):
    __tablename__ = "physical_copies"
    __table_args__ = (
        UniqueConstraint("id", "resource_id", name="uq_physical_copy_resource"),
        CheckConstraint(
            "condition_status IN ('new', 'good', 'fair', 'damaged', 'lost')",
            name="ck_copy_condition",
        ),
        CheckConstraint(
            "circulation_status IN ('available', 'borrowed', 'reserved', 'maintenance', 'lost')",
            name="ck_copy_circulation",
        ),
        Index("ix_physical_copies_resource_id", "resource_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), nullable=False)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    shelf_location: Mapped[str | None] = mapped_column(String(100))
    condition_status: Mapped[str] = mapped_column(String(30), nullable=False, default="good")
    circulation_status: Mapped[str] = mapped_column(String(30), nullable=False, default="available")
    acquired_at: Mapped[date | None] = mapped_column(Date)
