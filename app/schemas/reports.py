from pydantic import BaseModel
from decimal import Decimal


class MonthlyExpenseReport(BaseModel):
    """
    Represents the total expenses grouped by month.

    Attributes:
        month (str): Month in "YYYY-MM" format.
        total (Decimal): Total amount of expenses for that month.
    """
    month: str
    total: Decimal


class CategoryExpenseReport(BaseModel):
    """
    Represents the total expenses grouped by category.

    Attributes:
        category (str): Name of the category.
        total (Decimal): Total amount of expenses for that category.
    """
    category: str
    total: Decimal


class DailyExpenseReport(BaseModel):
    """
    Represents the total expenses for a specific day.

    Attributes:
        date (str): Date in ISO format "YYYY-MM-DD".
        total (Decimal): Total amount of expenses for that day.
    """
    date: str
    total: Decimal
