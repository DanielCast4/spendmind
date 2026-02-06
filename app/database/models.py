from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from .connection import Base

class Category(Base):
    """
    Represents a category for expenses.

    Attributes:
        id (int): Primary key for the category.
        name (str): Name of the category, must be unique and not null.
        essential (bool): Indicates if the category is considered essential. Defaults to False.
        expenses (list[Expense]): One-to-many relationship with Expense. Contains all expenses in this category.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    essential = Column(Boolean, default=False)
    expenses = relationship("Expense", back_populates="category")


class Expense(Base):
    """
    Represents a single expense entry.

    Attributes:
        id (int): Primary key for the expense.
        amount (Decimal): Amount of the expense. Cannot be null.
        description (str): Optional description of the expense.
        expense_date (date): Date of the expense. Cannot be null.
        category_id (int): Foreign key linking to the Category table.
        category (Category): Many-to-one relationship with Category.
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String)
    expense_date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="expenses")
