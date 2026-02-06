from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import and_

from app.database.connection import get_db
from app.database.models import Expense, Category
from app.schemas.expenses import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseWithCategoryResponse
)

# Create a router for expense-related endpoints
router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense in the database.

    Args:
        expense (ExpenseCreate): Data for the new expense from the request body.
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        Expense: The newly created expense object.
    """

    # Create a new Expense instance
    new_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        category_id=expense.category_id
    )

    # Add the expense to the database
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=list[ExpenseWithCategoryResponse])
def get_expenses(
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve expenses with optional filters.

    Args:
        start_date (date | None): Start date for filtering expenses.
        end_date (date | None): End date for filtering expenses.
        category_id (int | None): Filter expenses by category ID.
        limit (int): Maximum number of results to return. Default is 50.
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        list[ExpenseWithCategoryResponse]: List of expenses with category information.
    """

    # Build the base query joining Expense with Category
    query = (
        db.query(
            Expense.id,
            Expense.amount,
            Expense.description,
            Expense.expense_date,
            Expense.category_id,
            Category.name.label("category_name")
        )
        .join(Category)
    )

    # Filter by date range if both start_date and end_date are provided
    if start_date and end_date:
        query = query.filter(
            and_(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date
            )
        )

    # Filter by category if provided
    if category_id:
        query = query.filter(Expense.category_id == category_id)

    # Order by most recent expenses and apply limit
    return query.order_by(Expense.expense_date.desc()).limit(limit).all()
