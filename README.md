# Food Delivery Data Analytics and Business Intelligence Dashboard

A complete, end-to-end data analytics project analyzing food delivery orders,
customers, restaurants, delivery performance, ratings, and revenue — built to
the standard of a Data Analyst / Business Intelligence internship deliverable.

**Workflow:** Data Collection → Data Cleaning → Data Transformation →
Exploratory Data Analysis → SQL Analysis → Visualization → Power BI Dashboard
→ Business Insights

---

## 1. Project Objective

This project helps a food delivery business understand its sales performance,
customer behavior, restaurant performance, delivery efficiency, and overall
business trends — answering questions such as total revenue, average order
value, most popular categories, top restaurants, peak ordering hours,
delivery-time drivers, cancellation rates, and top customers.

## 2. Dataset

`data/raw_data.csv` — **9,270 synthetic-but-realistic order records** across
10 Indian cities, 220 restaurants, and 1,800 customers (Jan 2024 – Dec 2025),
generated with intentional real-world messiness: duplicate rows, missing
values, inconsistent city/payment-method casing and aliases, invalid ages,
negative amounts, and delivery-time outliers — so the cleaning stage has
genuine work to do.

`data/cleaned_data.csv` — the fully cleaned, validated, transformed dataset
(**9,000 rows, 34 columns**) used for all downstream analysis.

Fields include: `Order_ID, Order_Date, Order_Time, Customer_ID,
Customer_Name, Customer_Age, Customer_Gender, City, Restaurant_ID,
Restaurant_Name, Food_Category, Food_Item, Quantity, Price, Discount,
Delivery_Fee, Total_Amount, Payment_Method, Order_Status,
Delivery_Time_Minutes, Customer_Rating, Distance_KM, Order_Type` plus derived
columns (`Order_Year/Month/Weekday/Hour, Is_Weekend, Gross_Amount,
Net_Revenue, Discount_Pct, Is_Delayed, Is_Cancelled`).

## 3. Project Structure

```
food-delivery-analytics/
├── data/
│   ├── raw_data.csv                 # Raw, messy dataset (9,270 rows)
│   ├── cleaned_data.csv             # Cleaned, analysis-ready dataset (9,000 rows)
│   ├── customers_lookup.csv         # Customer reference data used during generation
│   └── restaurants_lookup.csv       # Restaurant reference data used during generation
│
├── notebooks/
│   └── food_delivery_analysis.ipynb # Full cleaning pipeline + EDA, executed with outputs
│
├── sql/
│   ├── food_delivery.db             # SQLite database (cleaned data loaded, indexed)
│   └── analysis_queries.sql         # 20 business-question SQL queries
│
├── visualizations/
│   └── charts/                      # 15 PNG charts covering Sales/Customers/Restaurants/Delivery/Orders
│
├── powerbi/
│   ├── powerbi_dataset.csv          # Import-ready dataset for Power BI Desktop
│   ├── dax_measures.txt             # All DAX measures for the dashboard
│   └── README.md                    # Page-by-page Power BI build guide (see note below)
│
├── reports/
│   ├── business_insights.md         # Observations + recommendations (What/Why/So what)
│   └── data_cleaning_log.txt        # Full log of every cleaning operation applied
│
├── scripts/
│   ├── 01_generate_raw.py           # Generates the raw messy dataset
│   ├── 02_clean_data.py             # Runs the cleaning pipeline (raw -> cleaned)
│   ├── 03_load_sql.py               # Loads cleaned data into SQLite
│   └── 04_visualize.py              # Generates all 15 charts
├── requirements.txt
└── README.md
```

## 4. How to Reproduce

```bash
pip install -r requirements.txt

python scripts/01_generate_raw.py     # -> data/raw_data.csv
python scripts/02_clean_data.py       # -> data/cleaned_data.csv, reports/data_cleaning_log.txt
python scripts/03_load_sql.py         # -> sql/food_delivery.db
python scripts/04_visualize.py        # -> visualizations/charts/*.png

# Full documented walkthrough (cleaning + EDA in one place):
jupyter nbconvert --to notebook --execute --inplace notebooks/food_delivery_analysis.ipynb

# SQL analysis:
sqlite3 sql/food_delivery.db < sql/analysis_queries.sql
```

## 5. Data Cleaning Summary

See `reports/data_cleaning_log.txt` for the complete log. Highlights:
- Removed 238 exact duplicate rows + 32 duplicate Order_IDs
- Standardized city names (e.g. Bombay → Mumbai, Bangalore → Bengaluru) and
  payment-method casing (e.g. COD → Cash On Delivery)
- Parsed two mixed date formats into a single datetime standard
- Corrected 45 invalid ages and 27 negative order amounts
- Capped 184 delivery-time outliers using the IQR method
- Treated ~3,300 missing cells using group-aware median/mode imputation
  (median delivery time per food category, median rating per restaurant, etc.)
- Added calculated columns: `Gross_Amount, Net_Revenue, Discount_Pct,
  Is_Delayed, Is_Cancelled`, plus calendar fields for time-based analysis

## 6. SQL Analysis

`sql/analysis_queries.sql` contains 20 queries covering total revenue, top
restaurants/customers, city-wise and monthly revenue, cancellation rate,
delivery-time analysis, customer segmentation (via `CASE`), payment-method
revenue share, peak ordering hours, weekday-vs-weekend comparison,
high-cancellation restaurants, and a distance-vs-delivery-time bucket
analysis — using `GROUP BY, ORDER BY, WHERE, HAVING, CASE, JOIN`-equivalent
patterns, and subqueries.

## 7. Power BI Dashboard

**Note:** Power BI Desktop is Windows-only and cannot run inside this (Linux)
environment, so a compiled `.pbix` file could not be produced here. Instead,
`powerbi/` contains everything needed to build it in a few minutes: the
import-ready dataset, every DAX measure, and a full page-by-page layout guide
(5 pages: Executive Overview, Sales Analysis, Customer Analysis, Restaurant
Analysis, Delivery Analysis) with the exact slicers, visuals, and interactive
features (drill-down, tooltips, cross-filtering, synced slicers) specified in
the project brief. Open `powerbi/README.md` and follow the steps.

## 8. Business Insights & Recommendations

Full analysis in `reports/business_insights.md`, structured as: **What
happened? → Why did it happen? → What does the data tell us? → What should
the business do?** Key findings include a strong distance–delivery-time
correlation (r = 0.73), a bimodal lunch/dinner ordering pattern, 94.6%
customer retention, and a small set of restaurants with disproportionately
high cancellation rates — each paired with a specific, data-backed
recommendation rather than generic advice.

## 9. Tech Stack

Python (Pandas, NumPy) · Jupyter Notebook · SQL (SQLite) · Matplotlib ·
Seaborn · Power BI
