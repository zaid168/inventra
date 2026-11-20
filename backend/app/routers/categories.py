from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Category
from app.schemas.categories import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):

    existing = db.query(Category).filter(
        Category.name == data.name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(name=data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):

    return db.query(Category).all()