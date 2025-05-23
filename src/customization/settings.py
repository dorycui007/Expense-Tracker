"""
settings.py: Manages user customization features for the Personal Expense Tracker.

This module provides functions to set and check budget limits, alerting users when exceeded.

Functions:
- check_budget(category, budget_limit): Checks if spending in a category exceeds the budget.
"""

from pymongo import MongoClient
import pandas as pd 

def check_budget(category, budget_limit):
    """
    Checks if spending in a category exceeds the specified budget limit.

    Retrieves data from MongoDB and prints an alert if the budget is exceeded.

    Args:
        category (str): The expense category (e.g., 'Food').
        budget_limit (float): The budget limit for the category.

    Returns:
        None
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find({"category": category}, {"amount": 1})))
    total_spent = df["amount"].sum()
    if total_spent > budget_limit:
        print(f"Alert: {category} spending (${total_spent:.2f}) exceeds budget (${budget_limit:.2f})")