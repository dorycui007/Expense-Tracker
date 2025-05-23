"""
charts.py: Generates visualizations for the Personal Expense Tracker.

This module provides functions to create charts, such as pie charts for category-wise and
payment method-wise spending, using aggregated general categories from MongoDB.

Functions:
- plot_category_pie(): Creates a pie chart of spending by aggregated general category.
- plot_payment_pie(): Creates a pie chart of spending by aggregated general payment method.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

def plot_category_pie():
    """
    Creates a pie chart showing spending distribution by aggregated general category.

    Retrieves data from MongoDB, aggregates 'lunch' and 'dinner' under 'Food', and uses
    Matplotlib to display the chart with general categories.

    Returns:
        None
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find()))
    category_sums = df.groupby("category")["amount"].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(category_sums, labels=category_sums.index, autopct="%1.1f%%")
    plt.title("Spending by Category")
    plt.savefig("category_pie.png")  # Save instead of show for compatibility

def plot_payment_pie():
    """
    Creates a pie chart showing spending distribution by aggregated general payment method.

    Retrieves data from MongoDB, aggregates 'TD debit' and 'td debit' under 'TD Debit', and
    uses Matplotlib to display the chart with general payment methods.

    Returns:
        None
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find()))
    payment_sums = df.groupby("payment_method")["amount"].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(payment_sums, labels=payment_sums.index, autopct="%1.1f%%")
    plt.title("Spending by Payment Method")
    plt.savefig("payment_pie.png")  # Save instead of show for compatibility