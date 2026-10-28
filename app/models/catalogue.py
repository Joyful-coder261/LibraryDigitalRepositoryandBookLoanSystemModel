"""Catalogue resources, authors, categories, and junction tables."""
from sqlalchemy import (
    CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, Numeric,
    SmallInteger, String, Text, UniqueConstraint, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(20), unique=True)
    resource_type: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    publisher: Mapped[str | None] = mapped_column(String(200))
    publication_year: Mapped[int | None] = mapped_column(SmallInteger)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    orcid: Mapped[str | None] = mapped_column(String(19), unique=True)


class ResourceAuthor(Base):
    __tablename__ = "resource_authors"
    __table_args__ = (
        UniqueConstraint("resource_id", "author_order", name="uq_resource_author_order"),
        CheckConstraint("author_order > 0", name="ck_author_order_positive"),
    )
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("authors.id"), primary_key=True)
    author_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))


class ResourceCategory(Base):
    __tablename__ = "resource_categories"
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("categories.id"), primary_key=True)
