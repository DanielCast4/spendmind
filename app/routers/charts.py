from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

import matplotlib.pyplot as plt
import io

from app.database.connection import get_db
from app.database.models import Expense

# Create a router for chart-related endpoints
router = APIRouter(prefix="/charts", tags=["Charts"])


@router.get("/monthly-expenses")
def monthly_expenses_chart(db: Session = Depends(get_db)):
    """
    Generates a line chart of monthly expenses.

    Args:
        db (Session): SQLAlchemy database session (injected by Depends).

    Returns:
        StreamingResponse: PNG image of the monthly expenses chart.
    """

    # Query to calculate total expenses grouped by year and month
    results = (
        db.query(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("total")
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    # Prepare labels and totals for plotting
    labels = [f"{int(r.month)}/{int(r.year)}" for r in results]
    totals = [r.total for r in results]

    # Create the plot
    plt.figure()
    plt.plot(labels, totals, marker="o")
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Total Spent")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Return the image as a streaming response
    return StreamingResponse(buf, media_type="image/png")
