"""Digital files associated with catalogue resources."""
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class DigitalAsset(Base):
    __tablename__ = "digital_assets"
    __table_args__ = (Index("ix_digital_assets_resource_id", "resource_id"),)
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), nullable=False)
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_uri: Mapped[str] = mapped_column(String(1000), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)
    access_level: Mapped[str] = mapped_column(String(30), nullable=False, default="restricted")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
