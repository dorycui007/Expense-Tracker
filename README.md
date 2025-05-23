# Personal Expense Tracker

A Python-based application for tracking personal expenses with features including a GUI interface, expense reporting, visualization, and machine learning capabilities for expense forecasting and anomaly detection.

## Features

- **GUI Interface**: Easy-to-use graphical interface for adding expenses
- **Expense Reporting**: View total expenses, category-wise spending, and payment method analysis
- **Data Visualization**: Interactive pie charts for expense categories and payment methods
- **Machine Learning**:
  - Expense forecasting using Prophet
  - Next month's expense prediction using linear regression
  - Anomaly detection using K-means clustering
- **Budget Management**: Set and monitor budget limits for different categories

## Requirements

- Python 3.11
- MongoDB
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd Personal-Expense-Tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv311
   source venv311/bin/activate  # On macOS/Linux
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install tkinter (if not already installed):
   ```bash
   brew install python-tk@3.11  # On macOS
   ```

5. Ensure MongoDB is running locally on port 27017

## Usage

Run the application:
```bash
python main.py
```

The application provides a menu-driven interface with the following options:
1. Add Expense (GUI)
2. View Report
3. View Category Pie Chart
4. Forecast Expenses
5. Predict Next Month's Expense
6. Detect Anomalies
7. Check Budget
8. Exit

## Project Structure

```
Personal-Expense-Tracker/
├── main.py                 # Application entry point
├── requirements.txt        # Python package dependencies
├── src/
│   ├── analysis/          # ML models and reporting
│   ├── interface/         # GUI implementation
│   ├── storage/           # Database operations
│   ├── visualization/     # Chart generation
│   └── customization/     # Budget settings
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 