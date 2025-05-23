# Entry point for the application

"""
main.py: Entry point for the Personal Expense Tracker.

This module orchestrates the application, allowing users to choose between GUI,
reports, visualizations, or machine learning features.

Functions:
- main(): Runs the main application loop.
"""

from src.interface.gui import create_gui
from src.analysis.reporting import generate_report
from src.visualization.charts import plot_category_pie
from src.analysis.ml_models import forecast_expenses, predict_expenses, detect_anomalies
from src.customization.settings import check_budget

def main():
    """
    Runs the main application loop, providing a command-line interface.

    Allows users to choose actions like adding expenses, viewing reports, or running ML models.

    Returns:
        None
    """
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense (GUI)")
        print("2. View Report")
        print("3. View Category Pie Chart")
        print("4. Forecast Expenses")
        print("5. Predict Next Month's Expense")
        print("6. Detect Anomalies")
        print("7. Check Budget")
        print("8. Exit")
        choice = input("Enter choice (1-8): ")
        
        if choice == "1":
            create_gui()
        elif choice == "2":
            generate_report()
        elif choice == "3":
            plot_category_pie()
        elif choice == "4":
            forecast = forecast_expenses()
            print(forecast.tail())
        elif choice == "5":
            prediction = predict_expenses()
            print(f"Predicted expense: ${prediction:.2f}")
        elif choice == "6":
            anomalies = detect_anomalies()
            print(anomalies)
        elif choice == "7":
            category = input("Enter category: ")
            budget = float(input("Enter budget limit: "))
            check_budget(category, budget)
        elif choice == "8":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()