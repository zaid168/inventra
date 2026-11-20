from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import StockTransaction

from app.db.session import get_db
from app.models import Item, Category
from app.schemas.items import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):

    existing = db.query(Item).filter(
        Item.sku == data.sku
    ).first()

    if existing:
        raise HTTPException(400, "SKU already exists")

    category = db.get(Category, data.category_id)

    if not category:
        raise HTTPException(404, "Category not found")

    item = Item(**data.model_dump())

    db.add(item)
    db.flush()

    from app.models import Inventory

    db.add(Inventory(item_id=item.id))

    db.commit()
    db.refresh(item)

    return item


@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):

    return db.query(Item).all()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):

    item = db.get(Item, item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    item = db.get(Item, item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    if item.inventory and item.inventory.quantity_on_hand > 0:
        raise HTTPException(400, "Cannot delete item with existing stock")

    if db.query(StockTransaction).filter(
        StockTransaction.item_id == item_id
    ).first():
        raise HTTPException(400, "Cannot delete item with transaction history")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted successfully"}
