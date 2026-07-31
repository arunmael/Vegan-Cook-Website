from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from backend.app.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """Stellt einem FastAPI-Endpunkt eine Datenbank-Session bereit."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def check_database_connection() -> None:
    """Prüft, ob die konfigurierte Datenbank erreichbar ist."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
