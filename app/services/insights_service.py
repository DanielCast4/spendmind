from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database.models import Expense, Category


def get_monthly_totals(db: Session):
    """
    Returns total expenses grouped by year and month.

    Args:
        db (Session): SQLAlchemy database session

    Returns:
        list: List of rows with 'year', 'month', and 'total' fields
    """
    return (
        db.query(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("total")
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )


def get_category_totals(db: Session):
    """
    Returns total expenses grouped by category.

    Args:
        db (Session): SQLAlchemy database session

    Returns:
        list: List of rows with 'name' (category) and 'total' fields
    """
    return (
        db.query(
            Category.name,
            func.sum(Expense.amount).label("total")
        )
        .join(Expense)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )


def generate_insights(db: Session) -> list[str]:
    """
    Generates textual insights based on the user's expenses.

    Args:
        db (Session): SQLAlchemy database session

    Returns:
        list[str]: List of insight strings
    """
    insights = []

    monthly = get_monthly_totals(db)
    categories = get_category_totals(db)

    if not monthly or not categories:
        return ["Not enough data to generate insights."]

    # 📈 Most expensive and least expensive month
    max_month = max(monthly, key=lambda x: x.total)
    min_month = min(monthly, key=lambda x: x.total)

    insights.append(
        f"📈 The month with the highest expenses was {int(max_month.month)}/{int(max_month.year)} "
        f"with a total of ${int(max_month.total):,}."
    )

    insights.append(
        f"📉 The month with the lowest expenses was {int(min_month.month)}/{int(min_month.year)} "
        f"with a total of ${int(min_month.total):,}."
    )

    # 🔥 Dominant category
    top_category = categories[0]
    insights.append(
        f"🔥 The category you spend the most on is '{top_category.name}', "
        f"accounting for ${int(top_category.total):,} of your total expenses."
    )

    # 💸 Rent weight (if present)
    total_spent = sum(m.total for m in monthly)

    for name, total in categories:
        if name.lower() in ("rent", "arriendo"):
            percent = (total / total_spent) * 100
            insights.append(
                f"🏠 Rent represents {percent:.1f}% of all your expenses."
            )

    # 📊 Monthly trend
    if len(monthly) >= 2:
        first = monthly[0].total
        last = monthly[-1].total
        change = ((last - first) / first) * 100

        trend = "increased" if change > 0 else "decreased"
        insights.append(
            f"📊 Your expenses have {trend} by {abs(change):.1f}% "
            f"over the analyzed period."
        )

    return insights
