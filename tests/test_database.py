"""
test_database.py: Unit tests for MongoDB operations in the Personal Expense Tracker.

This module tests the database functions to ensure data is correctly stored and retrieved.

Functions:
- test_add_expense(): Tests adding an expense to MongoDB.
"""

import pytest
from src.storage.database import add_expense_db, get_all_expenses

def test_add_expense():
    """
    Tests the add_expense_db function by adding an expense and verifying its presence.

    Ensures the expense is stored in MongoDB with correct category.

    Returns:
        None
    """
    add_expense_db("2025-05-20", 50.0, "Food", "Test", "Card")
    expenses = get_all_expenses()
    assert len(expenses) >= 1
    assert any(exp["category"] == "Food" for exp in expenses)

    from src.storage.database import add_expense_db
add_expense_db("2025-05-23", 20.0, "lunch", "Lunch at cafe", "td debit")
add_expense_db("2025-05-23", 25.0, "dinner", "Dinner at restaurant", "TD debit")
from src.analysis.reporting import generate_report
generate_report()  # Should show "Food" with $45 and "TD Debit" with $45
from src.visualization.charts import plot_category_pie, plot_payment_pie
plot_category_pie()  # Should show "Food" only
plot_payment_pie()  # Should show "TD Debit" only

test_add_expense()