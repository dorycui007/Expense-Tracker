"""
nlp.py: Handles automatic categorization for expense categories and payment methods in the Personal Expense Tracker.

This module provides functions to map user-entered expense categories and payment methods to general categories
(e.g., 'Food', 'TD Debit') using text similarity matching and NLP-based classification. It analyzes user inputs
and descriptions to ensure consistent categorization without extensive manual keyword lists. The module interacts
with MongoDB to retrieve training data for the NLP model.

Functions:
- get_general_category_from_similarity(category): Maps a user-entered category to a general category using text similarity.
- get_general_payment_method(payment_method): Maps a user-entered payment method to a general payment method using text similarity.
- train_category_classifier(): Trains a Naive Bayes model for expense category classification based on descriptions.
- train_payment_classifier(): Trains a Naive Bayes model for payment method classification based on descriptions.
- predict_and_refine_category(description, user_category, model, vectorizer): Refines the expense category using similarity and NLP.
- predict_and_refine_payment(description, user_payment, model, vectorizer): Refines the payment method using similarity and NLP.

Dependencies:
- sklearn.feature_extraction.text.TfidfVectorizer
- sklearn.naive_bayes.MultinomialNB
- pymongo.MongoClient
- pandas
- difflib (built-in)
"""

import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient
import pandas as pd

# Small set of example categories for similarity matching (not exhaustive)
CATEGORY_EXAMPLES = {
    "Food": ["drink", "lunch", "dinner", "groceries", "food"],
    "Transport": ["bus", "train", "taxi", "subway"],
    "Entertainment": ["movie", "game"],
    "Utilities": ["mobile", "internet"],
    "Miscellaneous": ["other"]
}

# Small set of example payment methods for similarity matching
PAYMENT_EXAMPLES = {
    "TD Debit": ["debit", "td debit"],
    "Cash": ["cash"],
    "Credit Card": ["credit", "visa", "mastercard"]
}

def get_general_category_from_similarity(category):
    """
    Maps a user-entered category to a general category using text similarity matching.

    Compares the input category to a small set of example categories using difflib's
    SequenceMatcher to compute similarity scores. Returns the general category with the
    highest similarity score above a threshold (0.8), or 'Miscellaneous' if no match.

    Args:
        category (str): The user-entered category (e.g., 'breakfast', 'coffe').

    Returns:
        str: The general category (e.g., 'Food', 'Transport') or 'Miscellaneous' if no match.

    Example:
        >>> get_general_category_from_similarity("lunch")
        'Food'
        >>> get_general_category_from_similarity("coffe")
        'Food'
        >>> get_general_category_from_similarity("random")
        'Miscellaneous'
    """
    category = category.lower().strip()
    best_score = 0
    best_category = "Miscellaneous"
    for general, examples in CATEGORY_EXAMPLES.items():
        for example in examples:
            score = difflib.SequenceMatcher(None, category, example).ratio()
            if score > best_score:
                best_score = score
                best_category = general
    return best_category if best_score > 0.8 else "Miscellaneous"

def get_general_payment_method(payment_method):
    """
    Maps a user-entered payment method to a general payment method using text similarity matching.

    Compares the input payment method to a small set of example payment methods using difflib's
    SequenceMatcher to compute similarity scores. Returns the general payment method with the
    highest similarity score above a threshold (0.8), or 'Miscellaneous' if no match.

    Args:
        payment_method (str): The user-entered payment method (e.g., 'td debit', 'debit').

    Returns:
        str: The general payment method (e.g., 'TD Debit', 'Cash') or 'Miscellaneous' if no match.

    Example:
        >>> get_general_payment_method("td debit")
        'TD Debit'
        >>> get_general_payment_method("Td debit")
        'TD Debit'
        >>> get_general_payment_method("random")
        'Miscellaneous'
    """
    payment_method = payment_method.lower().strip()
    best_score = 0
    best_payment = "Miscellaneous"
    for general, examples in PAYMENT_EXAMPLES.items():
        for example in examples:
            score = difflib.SequenceMatcher(None, payment_method, example).ratio()
            if score > best_score:
                best_score = score
                best_payment = general
    return best_payment if best_score > 0.8 else "Miscellaneous"

def train_category_classifier():
    """
    Trains a Naive Bayes classifier on expense descriptions to predict expense categories.

    Retrieves expense data from the MongoDB 'expense_tracker' database, using descriptions
    and their associated categories to train a text classification model. Used as a fallback
    when similarity matching fails to assign a general category.

    Returns:
        tuple: (MultinomialNB model, TfidfVectorizer) if sufficient data is available,
               (None, None) if insufficient data (fewer than 2 records).

    Example:
        >>> model, vectorizer = train_category_classifier()
        >>> model is None
        False  # Assuming sufficient data
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    data = pd.DataFrame(list(expenses.find({}, {"description": 1, "category": 1})))
    if len(data) < 2:
        return None, None  # Handle insufficient data
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(data["description"])
    y = data["category"]
    model = MultinomialNB()
    model.fit(X, y)
    return model, vectorizer

def train_payment_classifier():
    """
    Trains a Naive Bayes classifier on expense descriptions to predict payment methods.

    Retrieves expense data from the MongoDB 'expense_tracker' database, using descriptions
    and their associated payment methods to train a text classification model. Used as a fallback
    when similarity matching fails to assign a general payment method.

    Returns:
        tuple: (MultinomialNB model, TfidfVectorizer) if sufficient data is available,
               (None, None) if insufficient data (fewer than 2 records).

    Example:
        >>> model, vectorizer = train_payment_classifier()
        >>> model is None
        False  # Assuming sufficient data
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    data = pd.DataFrame(list(expenses.find({}, {"description": 1, "payment_method": 1})))
    if len(data) < 2:
        return None, None  # Handle insufficient data
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(data["description"])
    y = data["payment_method"]
    model = MultinomialNB()
    model.fit(X, y)
    return model, vectorizer

def predict_and_refine_category(description, user_category, model, vectorizer):
    """
    Refines a user-entered expense category by combining text similarity matching and NLP.

    First attempts to match the user-entered category to a general category using similarity
    matching. If no match is found, uses the NLP model to predict the category from the description.

    Args:
        description (str): The expense description (e.g., 'Morning meal at diner').
        user_category (str): The user-entered category (e.g., 'breakfast').
        model (MultinomialNB): Trained Naive Bayes model for categories, or None if not trained.
        vectorizer (TfidfVectorizer): Fitted vectorizer for categories, or None if not trained.

    Returns:
        str: The refined general category (e.g., 'Food').

    Example:
        >>> model, vectorizer = train_category_classifier()
        >>> predict_and_refine_category("Morning meal at diner", "breakfast", model, vectorizer)
        'Food'
        >>> predict_and_refine_category("Starbucks latte", "coffe", model, vectorizer)
        'Food'
    """
    # Try similarity matching first
    general_category = get_general_category_from_similarity(user_category)
    if general_category != "Miscellaneous":
        return general_category
    
    # Fallback to NLP prediction if similarity fails
    if model is not None and vectorizer is not None:
        X_new = vectorizer.transform([description])
        predicted_category = model.predict(X_new)[0]
        return predicted_category
    return "Miscellaneous"

def predict_and_refine_payment(description, user_payment, model, vectorizer):
    """
    Refines a user-entered payment method by combining text similarity matching and NLP.

    First attempts to match the user-entered payment method to a general payment method using
    similarity matching. If no match is found, uses the NLP model to predict the payment method
    from the description.

    Args:
        description (str): The expense description (e.g., 'Paid with TD debit card').
        user_payment (str): The user-entered payment method (e.g., 'td debit').
        model (MultinomialNB): Trained Naive Bayes model for payment methods, or None if not trained.
        vectorizer (TfidfVectorizer): Fitted vectorizer for payment methods, or None if not trained.

    Returns:
        str: The refined general payment method (e.g., 'TD Debit').

    Example:
        >>> model, vectorizer = train_payment_classifier()
        >>> predict_and_refine_payment("Paid with TD debit card", "td debit", model, vectorizer)
        'TD Debit'
        >>> predict_and_refine_payment("Coffee shop purchase", "debit", model, vectorizer)
        'TD Debit'
    """
    # Try similarity matching first
    general_payment = get_general_payment_method(user_payment)
    if general_payment != "Miscellaneous":
        return general_payment
    
    # Fallback to NLP prediction if similarity fails
    if model is not None and vectorizer is not None:
        X_new = vectorizer.transform([description])
        predicted_payment = model.predict(X_new)[0]
        return predicted_payment
    return "Miscellaneous"