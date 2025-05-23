# Machine learning (regression, clustering)

"""
ml_models.py: Implements machine learning models for the Personal Expense Tracker.

This module provides functions for time series forecasting, linear regression, and anomaly detection
using data from MongoDB.

Functions:
- forecast_expenses(): Forecasts future expenses using Prophet.
- predict_expenses(): Predicts next month's expenses using linear regression.
- detect_anomalies(): Detects unusual expenses using K-Means clustering.
"""

from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from pymongo import MongoClient
import pandas as pd
import numpy as np

def forecast_expenses():
    """
    Forecasts future expenses using Prophet.

    Retrieves data from MongoDB and predicts expenses for the next 30 days.

    Returns:
        pandas.DataFrame: Forecast with dates ('ds') and predicted amounts ('yhat').
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find({}, {"date": 1, "amount": 1})))
    df["ds"] = pd.to_datetime(df["date"])
    df["y"] = df["amount"]
    if len(df) < 2:
        return pd.DataFrame()  # Handle insufficient data
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(df[["ds", "y"]])
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]]

def predict_expenses():
    """
    Predicts expenses for 30 days in the future using linear regression.

    Retrieves data from MongoDB and fits a linear model based on days since earliest expense.

    Returns:
        float: Predicted expense amount.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find({}, {"date": 1, "amount": 1})))
    df["date"] = pd.to_datetime(df["date"])
    df["days"] = (df["date"] - df["date"].min()).dt.days
    X = df[["days"]]
    y = df["amount"]
    if len(df) < 2:
        return 0.0  # Handle insufficient data
    model = LinearRegression()
    model.fit(X, y)
    future_days = np.array([[df["days"].max() + 30]])
    prediction = model.predict(future_days)
    return prediction[0]

def detect_anomalies():
    """
    Detects anomalous expenses using K-Means clustering.

    Retrieves data from MongoDB, clusters expenses, and identifies outliers.

    Returns:
        pandas.DataFrame: DataFrame of anomalous expenses.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["expense_tracker"]
    expenses = db["expenses"]
    df = pd.DataFrame(list(expenses.find({}, {"amount": 1, "category": 1})))
    if len(df) < 3:
        return pd.DataFrame()  # Handle insufficient data
    # Drop the '_id' column (if present) so that fit_predict does not receive an ObjectId.
    if "_id" in df.columns:
        df = df.drop(columns=["_id"])
    df_encoded = pd.get_dummies(df, columns=["category"], drop_first=True)
    kmeans = KMeans(n_clusters=3)
    df["cluster"] = kmeans.fit_predict(df_encoded)
    distances = kmeans.transform(df_encoded)
    anomalies = df[distances.min(axis=1) > distances.mean()]
    return anomalies