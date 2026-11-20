from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    DateTime,
    ForeignKey,
    CheckConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    items = relationship(
        "Item",
        back_populates="category"
    )


class Item(Base):

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    item_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    barcode: Mapped[str | None] = mapped_column(
        String(150),
        unique=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="items"
    )

    inventory = relationship(
        "Inventory",
        back_populates="item",
        uselist=False
    )

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('RAW_MATERIAL', 'FINISHED_GOOD')",
            name="check_item_type"
        ),
    )


class Inventory(Base):

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id"),
        unique=True,
        nullable=False
    )

    quantity_on_hand: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        default=0,
        nullable=False
    )

    quantity_reserved: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        default=0,
        nullable=False
    )

    item = relationship(
        "Item",
        back_populates="inventory"
    )

    __table_args__ = (
        CheckConstraint(
            "quantity_on_hand >= 0",
            name="check_stock_nonnegative"
        ),
        CheckConstraint(
            "quantity_reserved >= 0",
            name="check_reserved_nonnegative"
        ),
        CheckConstraint(
            "quantity_reserved <= quantity_on_hand",
            name="check_reserved_not_exceed_stock"
        ),
    )


class StockTransaction(Base):

    __tablename__ = "stock_transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id"),
        nullable=False
    )

    transaction_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False
    )

    reference: Mapped[str | None] = mapped_column(
        String(100)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('STOCK_IN', 'STOCK_OUT', 'ADJUSTMENT')",
            name="check_transaction_type"
        ),
        CheckConstraint(
            "quantity > 0",
            name="check_transaction_quantity"
        ),
    )