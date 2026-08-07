from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Basisklasse für alle SQLAlchemy-Models."""


class User(Base):
    """SQLAlchemy-Model für die Tabelle `User`."""

    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    user_email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    user_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        )


