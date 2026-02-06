import random
from datetime import date, timedelta
from decimal import Decimal

from app.database.connection import SessionLocal
from app.database.models import Expense, Category  # Make sure you have a Category model

# =========================
# GENERAL CONFIGURATION
# =========================

NUM_EXPENSES = 200  # Number of expenses to generate

START_DATE = date(2025, 11, 1)
END_DATE = date(2026, 3, 31)

# Exact categories
CATEGORIES = {
    1: "Food",
    2: "Rent",
    3: "Transportation",
    4: "Leisure",
    5: "Health",
    6: "Education",
    7: "Shopping",
}

# Realistic spending ranges per category in USD
AMOUNT_RANGES_USD = {
    1: (3, 12),       # Food
    2: (220, 260),    # Rent (weekly or partial in USD)
    3: (2, 8),        # Transportation
    4: (4, 18),       # Leisure
    5: (10, 40),      # Health
    6: (16, 60),      # Education
    7: (8, 70)        # Shopping
}

# Example descriptions for each category
DESCRIPTIONS = {
    1: ["Lunch", "Dinner", "Groceries", "Supermarket"],
    2: ["Monthly rent"],
    3: ["Bus", "Taxi", "Weekly transport"],
    4: ["Cinema", "Out with friends", "Coffee"],
    5: ["Doctor appointment", "Medicines"],
    6: ["Online course", "Book"],
    7: ["Clothes", "Shoes", "Impulse purchase"]
}

# =========================
# HELPER FUNCTIONS
# =========================

def random_date(start: date, end: date) -> date:
    """
    Returns a random date between start and end dates.

    Args:
        start (date): Start date
        end (date): End date

    Returns:
        date: Random date within the given range
    """
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def random_amount(category_id: int) -> Decimal:
    """
    Returns a random amount in USD for a given category.

    Args:
        category_id (int): Category ID

    Returns:
        Decimal: Random expense amount
    """
    low, high = AMOUNT_RANGES_USD[category_id]
    return Decimal(round(random.uniform(low, high), 2))  # Round to 2 decimals


def random_description(category_id: int) -> str:
    """
    Returns a coherent description for a given category.

    Args:
        category_id (int): Category ID

    Returns:
        str: Random description
    """
    return random.choice(DESCRIPTIONS[category_id])

# =========================
# MAIN SCRIPT
# =========================

def create_categories(db):
    """
    Creates categories in the database if they do not already exist.

    Args:
        db (Session): Database session
    """
    for cat_id, name in CATEGORIES.items():
        # Avoid duplicates
        if not db.query(Category).filter_by(id=cat_id).first():
            db.add(Category(id=cat_id, name=name))
    db.commit()
    print("✅ Categories created successfully")


def generate_expenses():
    """
    Generates random expenses and inserts them into the database.
    """
    db = SessionLocal()

    try:
        create_categories(db)

        expenses = []

        for _ in range(NUM_EXPENSES):
            category_id = random.choice(list(CATEGORIES.keys()))
            expense = Expense(
                amount=random_amount(category_id),
                description=random_description(category_id),
                expense_date=random_date(START_DATE, END_DATE),
                category_id=category_id
            )
            expenses.append(expense)

        db.bulk_save_objects(expenses)
        db.commit()
        print(f"✅ {NUM_EXPENSES} expenses generated successfully")

    except Exception as e:
        db.rollback()
        print("❌ Error generating expenses:", e)

    finally:
        db.close()


if __name__ == "__main__":
    generate_expenses()
