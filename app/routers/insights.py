from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.insights_service import generate_insights

# Create a router for insights-related endpoints
router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/")
def get_insights(db: Session = Depends(get_db)):
    """
    Retrieve insights based on the user's expenses.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        dict: A dictionary containing insights generated from the expenses.
    """
    return {
        "insights": generate_insights(db)
    }
