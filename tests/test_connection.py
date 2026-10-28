"""Check the configured MySQL connection and list tables."""
from sqlalchemy import inspect, text
from app.database import make_engine
import app.models  # noqa: F401


def main():
    engine = make_engine()
    try:
        with engine.connect() as connection:
            print("Connected to MySQL successfully.")
            print("Server version:", connection.execute(text("SELECT VERSION()")).scalar())
            tables = sorted(inspect(connection).get_table_names())
            print("Tables currently in database:")
            for table in tables:
                print(" -", table)
            print(f"Table count (including alembic_version if present): {len(tables)}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
