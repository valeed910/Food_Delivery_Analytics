# Power BI Dashboard — Build Guide

> **Important:** Power BI Desktop only runs on Windows, so a `.pbix` binary cannot
> be compiled inside this (Linux) environment. This folder instead contains
> everything needed to build the dashboard in Power BI Desktop in minutes:
> the ready-to-import dataset, the exact data model, every DAX measure, and
> page-by-page layout instructions matching the project spec.

## 1. Files in this folder

| File | Purpose |
|---|---|
| `powerbi_dataset.csv` | Cleaned, analysis-ready dataset (9,000 rows, 34 columns) — same as `data/cleaned_data.csv`. Import this as the main table. |
| `dax_measures.txt` | All DAX measures to paste into Power BI's "New Measure" editor. |
| `README.md` | This build guide. |

## 2. Import & Data Model Setup

1. Open **Power BI Desktop** → **Get Data → Text/CSV** → select `powerbi_dataset.csv`.
2. In Power Query Editor, set data types:
   - `Order_Date` → Date
   - `Order_Hour`, `Order_Month`, `Order_Year`, `Quantity` → Whole Number
   - `Price`, `Discount`, `Delivery_Fee`, `Total_Amount`, `Net_Revenue`, `Gross_Amount`, `Distance_KM`, `Delivery_Time_Minutes`, `Customer_Rating` → Decimal Number
   - `Is_Weekend`, `Is_Delayed`, `Is_Cancelled` → True/False
3. Click **Close & Apply**.
4. Go to **Modeling → New Table** and create a proper **Date table** for time intelligence:
   ```dax
   DimDate = CALENDAR(MIN(powerbi_dataset[Order_Date]), MAX(powerbi_dataset[Order_Date]))
   ```
   Add `Month`, `MonthName`, `Year`, `Weekday` columns to `DimDate`, then relate
   `DimDate[Date]` (1) → `powerbi_dataset[Order_Date]` (many).
5. (Optional, recommended) Create a **Customer Segment** calculated column for
   segmentation used on Page 3:
   ```dax
   Customer_Segment =
   VAR CustTotal =
       CALCULATE(SUM(powerbi_dataset[Net_Revenue]),
           ALLEXCEPT(powerbi_dataset, powerbi_dataset[Customer_ID]))
   RETURN
   SWITCH(TRUE(),
       CustTotal >= 5000, "High Value",
       CustTotal >= 2000, "Medium Value",
       "Low Value")
   ```

## 3. DAX Measures

See `dax_measures.txt` for the full list (paste each into **New Measure**).
Core measures include: Total Revenue, Total Orders, Total Customers, Average
Order Value, Average Delivery Time, Cancellation Rate, Average Rating, Delayed
Order %, Revenue by City/Category/Restaurant, and Month-over-Month Revenue
Growth.

## 4. Page-by-Page Layout

### Page 1 — Executive Overview
- **KPI cards** (top row): `[Total Revenue]`, `[Total Orders]`, `[Total Customers]`, `[Avg Order Value]`, `[Avg Delivery Time]`, `[Cancellation Rate]`, `[Avg Rating]`
- **Line chart:** `Order_Date` (by month, from DimDate) vs `[Total Revenue]` → Monthly Revenue Trend
- **Bar chart:** `City` vs `[Total Orders]` → Orders by City
- **Donut chart:** `Food_Category` vs `[Total Revenue]` → Revenue by Food Category
- **Pie chart:** `Order_Status` (Count) → Order Status Distribution

### Page 2 — Sales Analysis
- Line chart: monthly sales (`[Total Revenue]` by month)
- Line/area chart: daily sales trend
- Bar chart: Revenue by City
- Bar chart: Top 10 Restaurants by Revenue
- Bar chart: Revenue by Food Category
- Card: `[Avg Order Value]`
- Bar/table: Discount analysis — `[Avg Discount %]` by Food_Category
- **Slicers:** `Order_Date` (date range), `City`, `Restaurant_Name`, `Food_Category`, `Payment_Method`

### Page 3 — Customer Analysis
- Card: `[Total Customers]`
- Donut: New vs Returning customers (use a calculated `Order_Count`-based flag)
- Table: Top 10 customers by `[Total Revenue]`
- Histogram/bar: Customer spending distribution
- Card: `[Avg Orders per Customer]`
- Bar/donut: `Customer_Segment` (Low/Medium/High Value) → count and revenue share

### Page 4 — Restaurant Analysis
- Bar chart: Top Restaurants by Revenue
- Bar chart: Top Restaurants by Order Count
- Table: Restaurant ratings (`Restaurant_Name`, `[Avg Rating]`, `[Total Orders]`)
- Bar chart: Average Order Value by Restaurant
- Table/matrix: Restaurant performance comparison (Revenue, Orders, Rating, Cancellation Rate side by side) — use this for the "flag restaurants above 15% cancellation" recommendation from `reports/business_insights.md`

### Page 5 — Delivery Analysis
- Card: `[Avg Delivery Time]`
- Bar chart: Avg Delivery Time by City
- Bar chart: Avg Delivery Time by Restaurant (top/bottom 10)
- Scatter chart: `Distance_KM` vs `Delivery_Time_Minutes` (add trendline) — Distance vs Delivery Time
- Card/gauge: `[Delayed Order %]`
- Card/gauge: `[Cancellation Rate]`

## 5. Interactive Features Checklist

- [ ] Add **Slicers** for Date, City, Restaurant, Food Category, Payment Method (sync across pages via **View → Sync Slicers**)
- [ ] Enable **drill-down** on the date hierarchy (Year → Month → Day) on all trend charts
- [ ] Enable default **tooltips** and add a tooltip page for restaurant details on hover
- [ ] Confirm **cross-filtering** works between visuals on the same page (default in Power BI — verify no visual has interactions disabled)
- [ ] Set a consistent color theme (View → Themes) across all 5 pages

## 6. Suggested Color Theme

Use a consistent theme aligned with the chart colors already used in
`visualizations/charts/`: primary `#2E86AB` (blue), accent `#F18F01` (orange),
alert `#C73E1D` (red, for delays/cancellations), success `#3B7A57` (green).
