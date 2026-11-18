# Business Loss Detective 🔍

A business analytics project that analyzes order data to find products with unusual cancellation patterns and estimate the sales value tied to them, so a business knows what to investigate first.

## Problem Statement
A business can have cancelled orders and low-profit products without knowing which one to look at first. This project uses transaction data to highlight unusual cancellation patterns and back each finding with evidence.

## Features
- Total orders, revenue, profit, cancellation rate and return rate
- Product-level cancellation, return and processing-time analysis
- Flags a product when it has enough orders and its cancellation rate is clearly above the overall rate
- Estimates the sales value tied to cancelled orders and ranks flagged products by it
- Interactive Streamlit dashboard with adjustable settings
- Explanations that keep **data-backed facts** separate from **unverified possible causes**
- Synthetic data generator (reproducible, with a planted problem to test detection)

## Technologies
Python, Pandas, Streamlit

## Project Files
- `generate_data.py` creates sample order data (`business_data.csv`)
- `analysis.py` holds all calculations and the explanation logic
- `app.py` is the Streamlit dashboard
- `business_data.csv` is the sample dataset (1,000 orders)

## How to Run
```
python -m pip install pandas streamlit
python generate_data.py
python -m streamlit run app.py
```

## Notes and Limitations
- The data is synthetic. One product (Webcam) was deliberately given a higher cancellation rate to test that the detector finds it.
- Explanations are rule-based. They list possible causes but do not prove them.
- Planned: returns-based analysis, AI-generated explanations, real data import.

## Author
Vyshnavi Durseti, B.Tech, NIT Warangal
