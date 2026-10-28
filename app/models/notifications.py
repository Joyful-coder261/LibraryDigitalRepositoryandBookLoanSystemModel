"""Notifications, user delivery preferences, and delivery attempts."""
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, Index, Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (Index("ix_notifications_user_id", "user_id"),)
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), nullable=False)
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    read_at: Mapped[datetime | None] = mapped_column(DateTime)


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), primary_key=True)
    email_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    personalization_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"
    __table_args__ = (
        CheckConstraint("delivery_status IN ('pending', 'sent', 'delivered', 'failed')", name="ck_delivery_status"),
        CheckConstraint("channel IN ('email', 'in_app', 'sms', 'whatsapp')", name="ck_delivery_channel"),
        Index("ix_notification_deliveries_notification_id", "notification_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    notification_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("notifications.id"), nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    delivery_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    attempted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime)
    error_message: Mapped[str | None] = mapped_column(Text)
