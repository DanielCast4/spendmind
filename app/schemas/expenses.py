from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class ExpenseCreate(BaseModel):
    """
    Data that the client must provide to create a new expense.
    """
    amount: Decimal
    description: str | None = None
    expense_date: date
    category_id: int


class ExpenseResponse(BaseModel):
    """
    Data returned by the API when retrieving an expense.
    """
    id: int
    amount: Decimal
    description: str | None
    expense_date: date
    category_id: int

    class Config:
        orm_mode = True  # Allows returning ORM objects directly


class ExpenseWithCategoryResponse(BaseModel):
    """
    Expense data including its category information.
    """
    id: int
    amount: Decimal
    description: str | None
    expense_date: date
    category_id: int
    category_name: str

    class Config:
        orm_mode = True  # Allows returning ORM objects directly
