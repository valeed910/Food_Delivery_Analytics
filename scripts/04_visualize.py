import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 110

CHART_DIR = "visualizations/charts"

df = pd.read_csv("data/cleaned_data.csv", parse_dates=["Order_Date"])
delivered = df[df["Order_Status"] != "Cancelled"].copy()

def savefig(name):
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/{name}.png", bbox_inches="tight")
    plt.close()
    print("saved", name)

# 1. Monthly revenue trend
monthly = delivered.groupby(delivered["Order_Date"].dt.to_period("M"))["Net_Revenue"].sum()
plt.figure(figsize=(11, 5))
monthly.index = monthly.index.astype(str)
sns.lineplot(x=monthly.index, y=monthly.values, marker="o", color="#2E86AB")
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
savefig("01_monthly_revenue_trend")

# 2. Revenue by city
city_rev = delivered.groupby("City")["Net_Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(x=city_rev.values, y=city_rev.index, color="#2E86AB")
plt.title("Revenue by City")
plt.xlabel("Revenue (₹)")
savefig("02_revenue_by_city")

# 3. Revenue by food category
cat_rev = delivered.groupby("Food_Category")["Net_Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(x=cat_rev.values, y=cat_rev.index, color="#F18F01")
plt.title("Revenue by Food Category")
plt.xlabel("Revenue (₹)")
savefig("03_revenue_by_food_category")

# 4. Order status distribution
plt.figure(figsize=(6, 6))
status_counts = df["Order_Status"].value_counts()
plt.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%",
        colors=sns.color_palette("deep"), startangle=90)
plt.title("Order Status Distribution")
savefig("04_order_status_distribution")

# 5. Top 10 restaurants by revenue
rest_rev = delivered.groupby("Restaurant_Name")["Net_Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
sns.barplot(x=rest_rev.values, y=rest_rev.index, color="#A23B72")
plt.title("Top 10 Restaurants by Revenue")
plt.xlabel("Revenue (₹)")
savefig("05_top10_restaurants_revenue")

# 6. Payment method distribution
plt.figure(figsize=(7, 5))
pm_counts = df["Payment_Method"].value_counts()
sns.barplot(x=pm_counts.values, y=pm_counts.index, color="#3B7A57")
plt.title("Payment Method Distribution")
plt.xlabel("Orders")
savefig("06_payment_method_distribution")

# 7. Peak ordering hours
plt.figure(figsize=(10, 5))
hour_counts = df["Order_Hour"].value_counts().sort_index()
sns.barplot(x=hour_counts.index, y=hour_counts.values, color="#C73E1D")
plt.title("Orders by Hour of Day (Peak Ordering Hours)")
plt.xlabel("Hour of Day (24h)")
plt.ylabel("Orders")
savefig("07_peak_ordering_hours")

# 8. Weekday vs weekend orders
plt.figure(figsize=(6, 5))
wk = df["Is_Weekend"].map({True: "Weekend", False: "Weekday"}).value_counts()
sns.barplot(x=wk.index, y=wk.values, color="#6A4C93")
plt.title("Weekday vs Weekend Orders")
plt.ylabel("Orders")
savefig("08_weekday_vs_weekend")

# 9. Distance vs delivery time scatter
plt.figure(figsize=(8, 6))
sample = delivered.sample(min(1500, len(delivered)), random_state=1)
sns.regplot(data=sample, x="Distance_KM", y="Delivery_Time_Minutes",
            scatter_kws={"alpha": 0.25, "s": 18, "color": "#2E86AB"},
            line_kws={"color": "#C73E1D"})
plt.title("Distance vs Delivery Time")
plt.xlabel("Distance (KM)")
plt.ylabel("Delivery Time (Minutes)")
savefig("09_distance_vs_delivery_time")

# 10. Average delivery time by city
city_dt = delivered.groupby("City")["Delivery_Time_Minutes"].mean().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(x=city_dt.values, y=city_dt.index, color="#F18F01")
plt.title("Average Delivery Time by City")
plt.xlabel("Avg Delivery Time (Minutes)")
savefig("10_avg_delivery_time_by_city")

# 11. Customer rating distribution
plt.figure(figsize=(8, 5))
sns.histplot(delivered["Customer_Rating"], bins=20, kde=True, color="#2E86AB")
plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
savefig("11_customer_rating_distribution")

# 12. Top 10 customers by spend
top_cust = delivered.groupby("Customer_Name")["Net_Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
sns.barplot(x=top_cust.values, y=top_cust.index, color="#A23B72")
plt.title("Top 10 Customers by Spend")
plt.xlabel("Total Spend (₹)")
savefig("12_top10_customers_spend")

# 13. Cancellation rate by restaurant (top 10 worst, min 20 orders)
rest_counts = df.groupby("Restaurant_Name").size()
valid_rests = rest_counts[rest_counts >= 20].index
sub = df[df["Restaurant_Name"].isin(valid_rests)]
cancel_rate = sub.groupby("Restaurant_Name")["Is_Cancelled"].mean().sort_values(ascending=False).head(10) * 100
plt.figure(figsize=(9, 5))
sns.barplot(x=cancel_rate.values, y=cancel_rate.index, color="#C73E1D")
plt.title("Top 10 Restaurants by Cancellation Rate (min 20 orders)")
plt.xlabel("Cancellation Rate (%)")
savefig("13_top10_cancellation_rate")

# 14. Daily revenue trend (rolling 7-day average)
daily = delivered.groupby(delivered["Order_Date"].dt.date)["Net_Revenue"].sum().sort_index()
daily_roll = daily.rolling(7).mean()
plt.figure(figsize=(11, 5))
plt.plot(daily.index, daily.values, alpha=0.3, color="#2E86AB", label="Daily Revenue")
plt.plot(daily_roll.index, daily_roll.values, color="#C73E1D", linewidth=2, label="7-day Avg")
plt.title("Daily Revenue Trend (with 7-day Rolling Average)")
plt.xlabel("Date")
plt.ylabel("Revenue (₹)")
plt.legend()
savefig("14_daily_revenue_trend")

# 15. Average order value by restaurant (top 10)
aov_rest = delivered.groupby("Restaurant_Name")["Net_Revenue"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
sns.barplot(x=aov_rest.values, y=aov_rest.index, color="#3B7A57")
plt.title("Top 10 Restaurants by Average Order Value")
plt.xlabel("Avg Order Value (₹)")
savefig("15_avg_order_value_by_restaurant")

print("All charts generated.")
