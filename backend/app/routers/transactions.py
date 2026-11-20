from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import StockTransaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):

    return db.query(StockTransaction).order_by(
        StockTransaction.created_at.desc()
    ).all()
