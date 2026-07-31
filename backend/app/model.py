from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Basisklasse für alle SQLAlchemy-Models."""


class Ingredient(Base):
    """SQLAlchemy-Model für die Tabelle `ingredient`."""

    __tablename__ = "ingredient"

    ingredient_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    ing_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
