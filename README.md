# Group 4 — Library Digital Repository and Book Loan System

Database-model starter project based on `Group4_Library_Database_Schema_Documentation.docx`.

**Scope:** SQLAlchemy models, MySQL connection configuration, Alembic migration setup, and basic verification. This does not implement routes, controllers, services, a frontend, or recommendation algorithms.

## Important configuration

1. Open this project folder in VS Code.
2. Create and activate a virtual environment (Windows PowerShell):

   ```powershell
   python -m venv .venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

   The `Set-ExecutionPolicy` command applies only to the current PowerShell process.

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to a new file named `.env`.
5. In `.env`, replace `REPLACE_WITH_YOUR_MYSQL_PASSWORD` with your actual MySQL password. Keep `DB_NAME=group4_library_db` unless you intentionally choose another database name. If you change it, use the same name consistently in MySQL and `.env`.
6. Create the database in MySQL Workbench or the MySQL client:

   ```sql
   CREATE DATABASE group4_library_db
     CHARACTER SET utf8mb4
     COLLATE utf8mb4_unicode_ci;
   ```

   Do not put SQL statements inside `.env`.

## Verify the Python models

From the project root, with `.venv` activated:

```powershell
python -c "import app.models; from app.database import Base; print(len(Base.metadata.tables)); print(sorted(Base.metadata.tables.keys()))"
```

The expected count is **25 tables**.

Run the basic SQLite model check:

```powershell
python -m pytest
```

SQLite is used only for a local structural test. It does not prove that the live MySQL database has been migrated.

## Verify the MySQL connection

After creating `.env` and the MySQL database:

```powershell
python tests/test_connection.py
```

If this fails, check that MySQL Server is running and that `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` are correct.

## Alembic migrations

The `migrations/` directory and the initial revision are included. Review `migrations/env.py` and `.env` before running a migration.

Check the current migration:

```powershell
python -m alembic current
```

Apply the included initial migration:

```powershell
python -m alembic upgrade head
```

Then verify in MySQL:

```sql
USE group4_library_db;
SHOW TABLES;
SHOW CREATE TABLE loans;
SHOW CREATE TABLE reservations;
```

Expected: 25 application tables plus `alembic_version`.

**Caution:** The included initial migration uses the SQLAlchemy metadata from the model files. Always keep models and migration in sync. Test against a disposable development database first. MySQL CHECK constraints require MySQL 8.0.16 or later. The live MySQL migration must be verified on your own machine.

## Database design notes

- The schema follows the uploaded documentation's 25-table dictionary.
- MySQL uses InnoDB, `utf8mb4`, unsigned BIGINT identifiers and UTC DATETIME convention; SQLite testing uses integer identifiers.
- Active loans use a generated `active_copy_id` and unique constraint to prevent two simultaneous active/overdue loans for the same physical copy.
- Reservations use a composite foreign key to ensure a fulfilled copy belongs to the reserved resource.
- `notification_preferences.personalization_consent` defaults to `False`. The application must check consent before collecting interaction events.
- Design limitations documented in the source include a separate work/edition distinction, publisher normalization, and consent history being deferred.
