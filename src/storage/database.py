"""
database.py: Handles MongoDB interactions for the Personal Expense Tracker.

This module provides functions to initialize the MongoDB connection, manage expense data,
and refine categories and payment methods using similarity matching and NLP.

Functions:
- init_db(): Initializes and returns the MongoDB database connection.
- add_expense_db(date, amount, category, description, payment_method, category_model, category_vectorizer, payment_model, payment_vectorizer): Adds an expense with refined category and payment method.
- get_all_expenses(): Retrieves all expenses from MongoDB.
"""

from pymongo import MongoClient
from src.analysis.nlp import get_general_category_from_similarity, get_general_payment_method, predict_and_refine_category, predict_and_refine_payment

def init_db():
    """
    Initializes the MongoDB connection and returns the database object.

    Returns:
        pymongo.database.Database: The MongoDB database object for 'expense_tracker'.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    return db

def add_expense_db(date, amount, category, description, payment_method, category_model=None, category_vectorizer=None, payment_model=None, payment_vectorizer=None):
    """
    Adds an expense to the MongoDB 'expenses' collection with refined category and payment method.

    Uses get_general_category_from_similarity for the initial category refinement and
    get_general_payment_method for the payment method. Falls back to NLP if needed.

    Args:
        date (str): Date of the expense (e.g., '2025-05-20').
        amount (float): Amount spent.
        category (str): User-entered category (e.g., 'Coffee').
        description (str): Description of the expense.
        payment_method (str): User-entered payment method (e.g., 'td debit').
        category_model (MultinomialNB, optional): Trained Naive Bayes model for categories.
        category_vectorizer (TfidfVectorizer, optional): Fitted vectorizer for categories.
        payment_model (MultinomialNB, optional): Trained Naive Bayes model for payment methods.
        payment_vectorizer (TfidfVectorizer, optional): Fitted vectorizer for payment methods.

    Returns:
        None
    """
    db = init_db()
    expenses = db["expenses"]
    refined_category = get_general_category_from_similarity(category)
    refined_payment = get_general_payment_method(payment_method)
    # Use predict_and_refine_* as fallback if similarity returns 'Miscellaneous'
    if refined_category == "Miscellaneous" and category_model and category_vectorizer:
        refined_category = predict_and_refine_category(description, category, category_model, category_vectorizer)
    if refined_payment == "Miscellaneous" and payment_model and payment_vectorizer:
        refined_payment = predict_and_refine_payment(description, payment_method, payment_model, payment_vectorizer)
    expense = {
        "date": date,
        "amount": float(amount),
        "category": refined_category,  # Store refined category
        "original_category": category,  # Store user-entered category for reference
        "description": description,
        "payment_method": refined_payment,  # Store refined payment method
        "original_payment_method": payment_method  # Store user-entered payment method for reference
    }
    expenses.insert_one(expense)

def get_all_expenses():
    """
    Retrieves all expenses from the MongoDB 'expenses' collection.

    Returns:
        list: List of expense documents.
    """
    db = init_db()
    expenses = db["expenses"]
    return list(expenses.find())