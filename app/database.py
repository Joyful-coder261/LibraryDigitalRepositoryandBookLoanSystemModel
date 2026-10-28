"""Database configuration shared by the SQLAlchemy models and Alembic."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import BigInteger, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# Use BIGINT on MySQL and INTEGER on SQLite so SQLite primary keys autoincrement
# correctly during local structural tests.
ID_TYPE = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_database_url() -> str:
    """Build the MySQL URL from .env without hard-coding credentials."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "group4_library_db")
    from urllib.parse import quote_plus
    return (
        f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{database}?charset=utf8mb4"
    )


def make_engine(url: str | None = None, *, echo: bool = False):
    """Create an engine; an explicit URL is useful for tests."""
    return create_engine(
        url or get_database_url(),
        echo=echo,
        pool_pre_ping=True,
        future=True,
    )


def get_session_factory(engine=None):
    """Return a SQLAlchemy session factory."""
    engine = engine or make_engine()
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
