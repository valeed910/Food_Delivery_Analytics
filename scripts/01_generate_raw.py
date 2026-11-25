"""
Generates a realistic, intentionally-messy raw food delivery orders dataset.
Rows: ~9000 (before duplicates are added) -> final raw file has duplicates,
missing values, inconsistent casing, and a few invalid values so that the
data-cleaning stage in the notebook has real work to do.
"""
import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)
np.random.seed(42)

N_BASE = 9000  # base unique-ish orders; duplicates added later

CITIES = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
          "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]

FOOD_CATEGORIES = {
    "North Indian": ["Butter Chicken", "Paneer Tikka Masala", "Dal Makhani", "Chole Bhature", "Rogan Josh"],
    "South Indian": ["Masala Dosa", "Idli Sambar", "Uttapam", "Medu Vada", "Curd Rice"],
    "Chinese": ["Veg Hakka Noodles", "Chilli Paneer", "Manchurian", "Fried Rice", "Spring Rolls"],
    "Fast Food": ["Cheese Burger", "French Fries", "Chicken Nuggets", "Veg Wrap", "Loaded Fries"],
    "Pizza": ["Margherita Pizza", "Farmhouse Pizza", "Pepperoni Pizza", "Paneer Tikka Pizza", "BBQ Chicken Pizza"],
    "Desserts": ["Gulab Jamun", "Chocolate Brownie", "Ice Cream Sundae", "Rasmalai", "Cheesecake"],
    "Beverages": ["Cold Coffee", "Masala Chai", "Fresh Lime Soda", "Milkshake", "Mango Lassi"],
    "Biryani": ["Chicken Biryani", "Mutton Biryani", "Veg Biryani", "Egg Biryani", "Hyderabadi Biryani"],
    "Healthy": ["Quinoa Salad", "Grilled Chicken Salad", "Sprouts Bowl", "Fruit Bowl", "Buddha Bowl"],
    "Mexican": ["Veg Burrito", "Chicken Tacos", "Nachos", "Quesadilla", "Burrito Bowl"],
}
CATEGORY_LIST = list(FOOD_CATEGORIES.keys())

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Wallet"]
ORDER_STATUS = ["Delivered", "Delivered", "Delivered", "Delivered", "Delivered",
                "Cancelled", "Delivered", "Delivered", "Delivered", "Delayed"]
ORDER_TYPE = ["Delivery", "Delivery", "Delivery", "Pickup"]
GENDERS = ["Male", "Female", "Other"]

# messy variants used to simulate inconsistent categorical entries
CITY_MESSY_MAP = {
    "Mumbai": ["mumbai", "MUMBAI", "Mumbai ", "Bombay"],
    "Bengaluru": ["bengaluru", "Bangalore", "BENGALURU", "bangalore "],
    "Delhi": ["delhi", "New Delhi", "DELHI"],
}
PAYMENT_MESSY_MAP = {
    "UPI": ["upi", "UPI ", "Upi"],
    "Cash on Delivery": ["COD", "cash on delivery", "cod"],
}

def messy_city(city):
    if city in CITY_MESSY_MAP and random.random() < 0.15:
        return random.choice(CITY_MESSY_MAP[city])
    return city

def messy_payment(pm):
    if pm in PAYMENT_MESSY_MAP and random.random() < 0.15:
        return random.choice(PAYMENT_MESSY_MAP[pm])
    return pm

# generate a pool of customers and restaurants so behaviour repeats realistically
N_CUSTOMERS = 1800
N_RESTAURANTS = 220

customers = []
for i in range(1, N_CUSTOMERS + 1):
    customers.append({
        "Customer_ID": f"CUST{i:05d}",
        "Customer_Name": fake.name(),
        "Customer_Age": int(np.clip(np.random.normal(31, 9), 16, 70)),
        "Customer_Gender": random.choices(GENDERS, weights=[0.52, 0.46, 0.02])[0],
        "City": random.choice(CITIES),
    })
customers_df = pd.DataFrame(customers)

restaurants = []
for i in range(1, N_RESTAURANTS + 1):
    cat = random.choice(CATEGORY_LIST)
    restaurants.append({
        "Restaurant_ID": f"REST{i:04d}",
        "Restaurant_Name": f"{fake.company().split(',')[0]} {random.choice(['Kitchen','Diner','Cafe','Express','House','Bistro'])}",
        "Primary_Category": cat,
        "City": random.choice(CITIES),
        "Base_Rating": round(np.clip(np.random.normal(4.0, 0.5), 2.5, 5.0), 1),
    })
restaurants_df = pd.DataFrame(restaurants)

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(1, N_BASE + 1):
    cust = customers_df.iloc[random.randrange(N_CUSTOMERS)]
    rest = restaurants_df.iloc[random.randrange(N_RESTAURANTS)]
    category = rest["Primary_Category"] if random.random() < 0.8 else random.choice(CATEGORY_LIST)
    food_item = random.choice(FOOD_CATEGORIES[category])

    order_date = start_date + timedelta(days=random.randint(0, date_range_days))
    # realistic bimodal ordering pattern: lunch peak (~13:00) and a larger dinner peak (~20:00)
    if random.random() < 0.32:
        hour = int(np.clip(np.random.normal(13, 1.3), 8, 16))
    else:
        hour = int(np.clip(np.random.normal(20, 1.6), 17, 23))
    minute = random.randint(0, 59)
    order_time = f"{hour:02d}:{minute:02d}:00"

    price = round(random.uniform(99, 799), 2)
    quantity = random.choices([1, 2, 3, 4], weights=[0.55, 0.28, 0.12, 0.05])[0]
    discount = round(price * random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2]), 2)
    delivery_fee = round(random.choice([0, 20, 25, 30, 40, 49]), 2)
    subtotal = price * quantity - discount
    total_amount = round(subtotal + delivery_fee, 2)

    distance_km = round(np.clip(np.random.exponential(4.5), 0.5, 25), 1)
    base_delivery_time = 15 + distance_km * 2.2
    delivery_time = int(np.clip(np.random.normal(base_delivery_time, 8), 10, 120))

    status = random.choice(ORDER_STATUS)
    if status == "Cancelled":
        rating = np.nan
        delivery_time_val = np.nan
    else:
        rating = round(np.clip(np.random.normal(rest["Base_Rating"], 0.6), 1, 5), 1)
        delivery_time_val = delivery_time

    order_type = random.choice(ORDER_TYPE)

    rows.append({
        "Order_ID": f"ORD{i:06d}",
        "Order_Date": order_date.strftime("%d-%m-%Y") if random.random() < 0.5 else order_date.strftime("%Y/%m/%d"),
        "Order_Time": order_time,
        "Customer_ID": cust["Customer_ID"],
        "Customer_Name": cust["Customer_Name"],
        "Customer_Age": cust["Customer_Age"],
        "Customer_Gender": cust["Customer_Gender"],
        "City": messy_city(cust["City"]),
        "Restaurant_ID": rest["Restaurant_ID"],
        "Restaurant_Name": rest["Restaurant_Name"],
        "Food_Category": category,
        "Food_Item": food_item,
        "Quantity": quantity,
        "Price": price,
        "Discount": discount,
        "Delivery_Fee": delivery_fee,
        "Total_Amount": total_amount,
        "Payment_Method": messy_payment(random.choice(PAYMENT_METHODS)),
        "Order_Status": status,
        "Delivery_Time_Minutes": delivery_time_val,
        "Customer_Rating": rating,
        "Distance_KM": distance_km,
        "Order_Type": order_type,
    })

df = pd.DataFrame(rows)

# ---- inject messiness ----

# 1. Missing values in several columns
for col, frac in [("Customer_Rating", 0.06), ("Delivery_Time_Minutes", 0.04),
                   ("Discount", 0.03), ("Customer_Age", 0.02), ("Payment_Method", 0.015),
                   ("Distance_KM", 0.01)]:
    idx = df.sample(frac=frac, random_state=random.randint(1, 9999)).index
    df.loc[idx, col] = np.nan

# 2. Duplicate rows (~3%)
dup_rows = df.sample(frac=0.03, random_state=7)
df = pd.concat([df, dup_rows], ignore_index=True)

# 3. Invalid / outlier values
invalid_idx = df.sample(frac=0.005, random_state=11).index
df.loc[invalid_idx, "Customer_Age"] = random.choice([-5, 0, 150])
outlier_idx = df.sample(frac=0.004, random_state=13).index
df.loc[outlier_idx, "Delivery_Time_Minutes"] = df.loc[outlier_idx, "Delivery_Time_Minutes"].apply(
    lambda x: random.choice([250, 300, 400]))
neg_idx = df.sample(frac=0.003, random_state=17).index
df.loc[neg_idx, "Total_Amount"] = -abs(df.loc[neg_idx, "Total_Amount"])

# 4. Inconsistent text casing in a few more places
case_idx = df.sample(frac=0.05, random_state=19).index
df.loc[case_idx, "Food_Category"] = df.loc[case_idx, "Food_Category"].str.upper()

# shuffle rows so duplicates aren't neatly at the end
df = df.sample(frac=1.0, random_state=99).reset_index(drop=True)

df.to_csv("data/raw_data.csv", index=False)
customers_df.to_csv("data/customers_lookup.csv", index=False)
restaurants_df.to_csv("data/restaurants_lookup.csv", index=False)

print("Raw rows:", len(df))
print(df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())
