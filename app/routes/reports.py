from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.database.models import Expense, Category
from app.schemas.reports import (
    MonthlyExpenseReport,
    CategoryExpenseReport,
    DailyExpenseReport
)

# Create a router for report-related endpoints
router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/monthly", response_model=list[MonthlyExpenseReport])
def monthly_expenses(db: Session = Depends(get_db)):
    """
    Returns total expenses grouped by month.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        list[MonthlyExpenseReport]: List of total expenses per month.
    """

    results = (
        db.query(
            func.to_char(func.date_trunc("month", Expense.expense_date), "YYYY-MM")
            .label("month"),
            func.sum(Expense.amount).label("total")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    return results


@router.get("/by-category", response_model=list[CategoryExpenseReport])
def expenses_by_category(db: Session = Depends(get_db)):
    """
    Returns total expenses grouped by category.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        list[CategoryExpenseReport]: List of total expenses per category.
    """

    results = (
        db.query(
            Category.name.label("category"),
            func.sum(Expense.amount).label("total")
        )
        .join(Expense)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return results


@router.get("/daily", response_model=list[DailyExpenseReport])
def most_expensive_days(db: Session = Depends(get_db)):
    """
    Returns the days with the highest total expenses.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        list[DailyExpenseReport]: Top 10 days with the highest total expenses.
    """

    results = (
        db.query(
            Expense.expense_date.label("date"),
            func.sum(Expense.amount).label("total")
        )
        .group_by(Expense.expense_date)
        .order_by(func.sum(Expense.amount).desc())
        .limit(10)
        .all()
    )

    # Convert results to a JSON-friendly format
    return [
        {
            "date": row.date.isoformat(),
            "total": float(row.total)
        }
        for row in results
    ]
