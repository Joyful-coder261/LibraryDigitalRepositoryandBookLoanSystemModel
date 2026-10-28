"""Local structural tests; these do not verify a live MySQL server."""
from sqlalchemy import create_engine, inspect
from app.database import Base
import app.models  # noqa: F401


EXPECTED_TABLES = {
    "roles", "permissions", "user_roles", "role_permissions", "users",
    "resources", "authors", "resource_authors", "categories", "resource_categories",
    "topics", "resource_topics", "physical_copies", "digital_assets", "loans",
    "reservations", "user_interactions", "user_interests", "recommendations",
    "knowledge_links", "notifications", "notification_preferences",
    "notification_deliveries", "audit_logs", "login_events",
}


def test_all_25_tables_are_registered():
    assert len(Base.metadata.tables) == 25
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_sqlite_can_create_schema():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    assert set(inspector.get_table_names()) == EXPECTED_TABLES
    engine.dispose()
