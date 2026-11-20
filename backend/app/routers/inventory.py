from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Inventory, StockTransaction

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/")
def get_inventory(db: Session = Depends(get_db)):

    records = db.query(Inventory).all()

    return [
        {
            "item_id": record.item_id,
            "item_name": record.item.name,
            "sku": record.item.sku,
            "quantity_on_hand": record.quantity_on_hand,
            "quantity_reserved": record.quantity_reserved,
            "available_quantity": (
                record.quantity_on_hand - record.quantity_reserved
            )
        }
        for record in records
    ]


@router.post("/{item_id}/receive")
def receive_stock(
    item_id: int,
    quantity: Decimal,
    db: Session = Depends(get_db)
):

    inventory = db.query(Inventory).filter(
        Inventory.item_id == item_id
    ).with_for_update().first()

    if not inventory:
        raise HTTPException(404, "Inventory record not found")

    if quantity <= 0:
        raise HTTPException(400, "Quantity must be positive")

    inventory.quantity_on_hand += quantity

    transaction = StockTransaction(
        item_id=item_id,
        transaction_type="STOCK_IN",
        quantity=quantity
    )

    db.add(transaction)
    db.commit()

    return {"message": "Stock received successfully"}


@router.post("/{item_id}/issue")
def issue_stock(
    item_id: int,
    quantity: Decimal,
    db: Session = Depends(get_db)
):

    inventory = db.query(Inventory).filter(
        Inventory.item_id == item_id
    ).with_for_update().first()

    if not inventory:
        raise HTTPException(404, "Inventory record not found")

    if quantity <= 0:
        raise HTTPException(400, "Quantity must be positive")

    available = (
        inventory.quantity_on_hand - inventory.quantity_reserved
    )

    if quantity > available:
        raise HTTPException(400, "Insufficient available stock")

    inventory.quantity_on_hand -= quantity

    transaction = StockTransaction(
        item_id=item_id,
        transaction_type="STOCK_OUT",
        quantity=quantity
    )

    db.add(transaction)
    db.commit()

    return {"message": "Stock issued successfully"}
