"""Initial 25-table library schema.

Revision ID: e7f05f915f31
Revises:
"""
from alembic import op
from app.database import Base
import app.models  # noqa: F401 - register all models

revision = "e7f05f915f31"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all application tables from the reviewed SQLAlchemy metadata."""
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind, checkfirst=True)


def downgrade() -> None:
    """Drop application tables in dependency-aware order."""
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind, checkfirst=True)
