# Business Loss Detective 🔍

An evidence-based business analytics project that analyzes order data to identify potential business problems and help prioritize further investigation.

## 🎯 Problem Statement

Businesses may experience cancelled orders, low product profitability, and other operational issues without knowing which areas need attention first.

Business Loss Detective analyzes transaction data to highlight unusual cancellation patterns and provide data-backed insights.

## ✨ Features

- Calculates total orders, revenue, profit, and cancellation rates.
- Analyzes order and cancellation patterns for individual products.
- Flags products whose cancellation rates exceed the overall business cancellation rate.
- Estimates the order value associated with cancelled orders.
- Generates sample transaction data for testing.

## 🛠️ Technologies Used

- Python
- Pandas
- CSV data processing

## 📂 Project Files

- `app.py` — analyzes transaction data and calculates business metrics.
- `generate_data.py` — generates sample order data.
- `business_data.csv` — sample dataset containing 1,000 orders.

## 🚀 How to Run

1. Install Python.
2. Install Pandas:

   `python -m pip install pandas`

3. Generate the sample dataset:

   `python generate_data.py`

4. Run the analysis:

   `python app.py`

## 🔍 Current Scope

This is an ongoing project. The current version focuses on transaction analysis and product-level cancellation detection. Dashboard features and AI-assisted explanations are planned improvements.

## 👩‍💻 Author

Vyshnavi Durseti  
B.Tech, NIT Warangal
