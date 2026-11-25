"""
Data Cleaning Pipeline for the Food Delivery Analytics project.
Reads data/raw_data.csv, performs cleaning/transformation steps, writes
data/cleaned_data.csv, and prints a log of every operation + row counts
(also saved to reports/data_cleaning_log.txt for documentation).
"""
import pandas as pd
import numpy as np

LOG = []
def log(msg):
    print(msg)
    LOG.append(msg)

RAW_PATH = "data/raw_data.csv"
CLEAN_PATH = "data/cleaned_data.csv"

df = pd.read_csv(RAW_PATH)
log(f"Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------
# 1. Remove exact duplicate rows
# ---------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
log(f"1. Removed exact duplicate rows: {before - len(df)} removed -> {len(df)} rows remain")

# Also drop duplicate Order_IDs (keep first occurrence) since Order_ID should be unique
before = len(df)
df = df.drop_duplicates(subset="Order_ID", keep="first")
log(f"   Removed duplicate Order_IDs (keeping first): {before - len(df)} removed -> {len(df)} rows remain")

# ---------------------------------------------------------------
# 2. Standardize categorical text values
# ---------------------------------------------------------------
df["City"] = df["City"].str.strip().str.title()
city_fix = {"Bombay": "Mumbai", "New Delhi": "Delhi", "Bangalore": "Bengaluru"}
df["City"] = df["City"].replace(city_fix)
log("2. Standardized City values: trimmed whitespace, title-cased, mapped aliases "
    "(Bombay->Mumbai, New Delhi->Delhi, Bangalore->Bengaluru)")

df["Payment_Method"] = df["Payment_Method"].str.strip().str.upper()
payment_fix = {"COD": "CASH ON DELIVERY", "UPI": "UPI"}
df["Payment_Method"] = df["Payment_Method"].replace(payment_fix)
df["Payment_Method"] = df["Payment_Method"].str.title()
df["Payment_Method"] = df["Payment_Method"].replace({"Upi": "UPI"})
log("2b. Standardized Payment_Method values (COD -> Cash On Delivery, casing normalized)")

df["Food_Category"] = df["Food_Category"].str.strip().str.title()
log("2c. Standardized Food_Category casing (title case)")

df["Customer_Gender"] = df["Customer_Gender"].str.strip().str.title()
df["Order_Status"] = df["Order_Status"].str.strip().str.title()
df["Order_Type"] = df["Order_Type"].str.strip().str.title()
log("2d. Standardized Customer_Gender, Order_Status, Order_Type casing")

# ---------------------------------------------------------------
# 3. Date & time formatting
# ---------------------------------------------------------------
def parse_date(val):
    for fmt in ("%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["Order_Date"] = df["Order_Date"].apply(parse_date)
unparsed = df["Order_Date"].isna().sum()
log(f"3. Parsed Order_Date from mixed formats (DD-MM-YYYY and YYYY/MM/DD) into datetime; "
    f"{unparsed} rows could not be parsed")

df["Order_Time"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S", errors="coerce").dt.time
log("3b. Converted Order_Time strings to time objects")

# derive calendar fields for later grouping
df["Order_Year"] = df["Order_Date"].dt.year
df["Order_Month"] = df["Order_Date"].dt.month
df["Order_Month_Name"] = df["Order_Date"].dt.strftime("%b %Y")
df["Order_Weekday"] = df["Order_Date"].dt.day_name()
df["Order_Hour"] = df["Order_Time"].apply(lambda t: t.hour if pd.notna(t) else np.nan)
df["Is_Weekend"] = df["Order_Weekday"].isin(["Saturday", "Sunday"])
log("3c. Derived calculated columns: Order_Year, Order_Month, Order_Month_Name, "
    "Order_Weekday, Order_Hour, Is_Weekend")

# ---------------------------------------------------------------
# 4. Data type correction
# ---------------------------------------------------------------
numeric_cols = ["Customer_Age", "Quantity", "Price", "Discount", "Delivery_Fee",
                 "Total_Amount", "Delivery_Time_Minutes", "Customer_Rating", "Distance_KM"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
log(f"4. Enforced numeric dtype on: {', '.join(numeric_cols)}")

# ---------------------------------------------------------------
# 5. Invalid-value detection & correction
# ---------------------------------------------------------------
invalid_age_mask = (df["Customer_Age"] < 10) | (df["Customer_Age"] > 90)
n_invalid_age = invalid_age_mask.sum()
df.loc[invalid_age_mask, "Customer_Age"] = np.nan
log(f"5. Flagged {n_invalid_age} invalid Customer_Age values (<10 or >90) and set to NaN")

neg_amount_mask = df["Total_Amount"] < 0
n_neg = neg_amount_mask.sum()
df.loc[neg_amount_mask, "Total_Amount"] = df.loc[neg_amount_mask, "Total_Amount"].abs()
log(f"5b. Corrected {n_neg} negative Total_Amount values by taking absolute value")

# ---------------------------------------------------------------
# 6. Outlier detection (IQR method) on Delivery_Time_Minutes
# ---------------------------------------------------------------
q1 = df["Delivery_Time_Minutes"].quantile(0.25)
q3 = df["Delivery_Time_Minutes"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
outlier_mask = df["Delivery_Time_Minutes"] > upper_bound
n_outliers = outlier_mask.sum()
log(f"6. Detected {n_outliers} Delivery_Time_Minutes outliers above IQR upper bound "
    f"({upper_bound:.1f} min) — capped at upper bound")
df.loc[outlier_mask, "Delivery_Time_Minutes"] = upper_bound

# ---------------------------------------------------------------
# 7. Missing-value treatment
# ---------------------------------------------------------------
before_na = df.isna().sum().sum()

# Age: fill with median age per gender
df["Customer_Age"] = df.groupby("Customer_Gender")["Customer_Age"].transform(
    lambda s: s.fillna(s.median()))
df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median()).round().astype("Int64")

# Discount: assume missing means no discount applied
df["Discount"] = df["Discount"].fillna(0)

# Distance: fill with median distance
df["Distance_KM"] = df["Distance_KM"].fillna(df["Distance_KM"].median())

# Payment method: fill with mode
df["Payment_Method"] = df["Payment_Method"].fillna(df["Payment_Method"].mode()[0])

# Delivery time & rating: only meaningful for Delivered orders; for Cancelled orders
# these stay NaN (correct, not missing data). For Delivered/Delayed orders with NaN,
# fill using restaurant/category median.
mask_should_have_time = df["Order_Status"] != "Cancelled"
df.loc[mask_should_have_time, "Delivery_Time_Minutes"] = (
    df.loc[mask_should_have_time]
      .groupby("Food_Category")["Delivery_Time_Minutes"]
      .transform(lambda s: s.fillna(s.median()))
)
df.loc[mask_should_have_time, "Customer_Rating"] = (
    df.loc[mask_should_have_time]
      .groupby("Restaurant_ID")["Customer_Rating"]
      .transform(lambda s: s.fillna(s.median()))
)
# any remaining NaN ratings (restaurant had no valid ratings at all) -> overall median
df["Customer_Rating"] = df["Customer_Rating"].fillna(df["Customer_Rating"].median())
df["Delivery_Time_Minutes"] = df["Delivery_Time_Minutes"].where(
    df["Order_Status"] == "Cancelled", df["Delivery_Time_Minutes"].fillna(df["Delivery_Time_Minutes"].median()))

after_na = df.isna().sum().sum()
log(f"7. Missing-value treatment complete: {before_na} missing cells -> {after_na} missing cells "
    f"remaining (remaining NaNs are Delivery_Time_Minutes/Customer_Rating for Cancelled orders, "
    f"which is expected — cancelled orders are never delivered or rated)")

# ---------------------------------------------------------------
# 8. Calculated / derived columns for analysis
# ---------------------------------------------------------------
df["Gross_Amount"] = (df["Price"] * df["Quantity"]).round(2)
df["Net_Revenue"] = (df["Total_Amount"]).round(2)
df["Discount_Pct"] = np.where(df["Gross_Amount"] > 0,
                               (df["Discount"] / df["Gross_Amount"] * 100).round(2), 0)
df["Is_Delayed"] = df["Delivery_Time_Minutes"] > 45  # business threshold
df["Is_Cancelled"] = df["Order_Status"] == "Cancelled"
log("8. Added calculated columns: Gross_Amount, Net_Revenue, Discount_Pct, "
    "Is_Delayed (>45 min), Is_Cancelled")

# ---------------------------------------------------------------
# 9. Validate numerical fields (sanity bounds)
# ---------------------------------------------------------------
assert (df["Quantity"] >= 1).all() or df["Quantity"].isna().any(), "Quantity should be >= 1"
assert (df["Total_Amount"] >= 0).all(), "Total_Amount should be non-negative after cleaning"
assert (df["Customer_Rating"].dropna().between(1, 5)).all(), "Ratings should be within 1-5"
log("9. Validated numerical fields: Quantity >= 1, Total_Amount >= 0, Rating within 1-5 — all passed")

# ---------------------------------------------------------------
# Final column ordering & save
# ---------------------------------------------------------------
df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
df = df.sort_values("Order_ID").reset_index(drop=True)

df.to_csv(CLEAN_PATH, index=False)
log(f"\nFinal cleaned dataset saved: {df.shape[0]} rows, {df.shape[1]} columns -> {CLEAN_PATH}")

with open("reports/data_cleaning_log.txt", "w") as f:
    f.write("\n".join(LOG))
