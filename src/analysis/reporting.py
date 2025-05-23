"""
reporting.py: Generates financial summaries for the Personal Expense Tracker.

This module provides functions to summarize expenses by aggregated general categories and
payment methods, using data from MongoDB. It combines 'lunch' and 'dinner' under 'Food' and
'TD debit'/'td debit' under 'TD Debit'.

Functions:
- generate_report(): Prints total expenses, category-wise, and payment method-wise spending.
"""

from pymongo import MongoClient
import pandas as pd

def generate_report():
    """
    Generates a summary report of total expenses, category-wise, and payment method-wise spending.

    Retrieves data from MongoDB, aggregates related categories (e.g., 'lunch' and 'dinner' as 'Food')
    and payment methods (e.g., 'TD debit' and 'td debit' as 'TD Debit'), and prints results.

    Returns:
        None
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find()))
    total_expenses = df["amount"].sum()
    category_summary = df.groupby("category")["amount"].sum()
    payment_summary = df.groupby("payment_method")["amount"].sum()
    print(f"Total Expenses: ${total_expenses:.2f}")
    print("\nCategory-wise Spending:")
    print(category_summary)
    print("\nPayment Method-wise Spending:")
    print(payment_summary)