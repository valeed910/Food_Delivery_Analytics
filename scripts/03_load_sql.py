import pandas as pd
import sqlite3

df = pd.read_csv("data/cleaned_data.csv")
conn = sqlite3.connect("sql/food_delivery.db")
df.to_sql("orders", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX IF NOT EXISTS idx_city ON orders(City)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_restaurant ON orders(Restaurant_ID)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_customer ON orders(Customer_ID)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON orders(Order_Status)")
conn.commit()

cur = conn.execute("SELECT COUNT(*) FROM orders")
print("Rows loaded into SQLite 'orders' table:", cur.fetchone()[0])
conn.close()
