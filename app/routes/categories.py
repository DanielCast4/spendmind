from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Category
from app.schemas.categories import CategoryCreate, CategoryResponse

# Create a router for category-related endpoints
router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    Prevents duplicate categories.

    Args:
        category (CategoryCreate): Category data from the request body.
        db (Session): SQLAlchemy database session (injected by Depends).

    Raises:
        HTTPException: If a category with the same name already exists.

    Returns:
        Category: The newly created category.
    """

    # Check if a category with the same name already exists
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    # Create a new category instance
    new_category = Category(
        name=category.name,
        essential=category.essential
    )

    # Add and commit the new category to the database
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        list[Category]: List of all categories ordered by name.
    """
    return db.query(Category).order_by(Category.name).all()
