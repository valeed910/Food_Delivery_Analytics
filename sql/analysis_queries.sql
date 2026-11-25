-- ============================================================
-- Food Delivery Analytics — SQL Analysis Queries
-- Database: sql/food_delivery.db (SQLite)  |  Table: orders
-- ============================================================

-- 1. Total revenue (delivered orders only — cancelled orders generate no revenue)
SELECT ROUND(SUM(Net_Revenue), 2) AS Total_Revenue
FROM orders
WHERE Order_Status != 'Cancelled';

-- 2. Total number of orders (all statuses)
SELECT COUNT(*) AS Total_Orders FROM orders;

-- 3. Average order value (delivered orders)
SELECT ROUND(AVG(Net_Revenue), 2) AS Avg_Order_Value
FROM orders
WHERE Order_Status != 'Cancelled';

-- 4. Top 10 restaurants by revenue
SELECT Restaurant_Name,
       COUNT(*) AS Total_Orders,
       ROUND(SUM(Net_Revenue), 2) AS Total_Revenue
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Restaurant_Name
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 5. Top 10 customers by total spend
SELECT Customer_ID, Customer_Name,
       COUNT(*) AS Orders_Placed,
       ROUND(SUM(Net_Revenue), 2) AS Total_Spend
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Customer_ID, Customer_Name
ORDER BY Total_Spend DESC
LIMIT 10;

-- 6. Most popular food categories (by order count and revenue)
SELECT Food_Category,
       COUNT(*) AS Orders,
       ROUND(SUM(Net_Revenue), 2) AS Revenue
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Food_Category
ORDER BY Orders DESC;

-- 7. City-wise revenue
SELECT City,
       COUNT(*) AS Orders,
       ROUND(SUM(Net_Revenue), 2) AS Revenue,
       ROUND(AVG(Net_Revenue), 2) AS Avg_Order_Value
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY City
ORDER BY Revenue DESC;

-- 8. Monthly sales trend
SELECT Order_Month_Name,
       COUNT(*) AS Orders,
       ROUND(SUM(Net_Revenue), 2) AS Revenue
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year, Order_Month;

-- 9. Daily order trend (top 15 busiest days)
SELECT Order_Date,
       COUNT(*) AS Orders,
       ROUND(SUM(Net_Revenue), 2) AS Revenue
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Order_Date
ORDER BY Orders DESC
LIMIT 15;

-- 10. Cancelled orders — count and percentage of total
SELECT
    (SELECT COUNT(*) FROM orders WHERE Order_Status = 'Cancelled') AS Cancelled_Orders,
    (SELECT COUNT(*) FROM orders) AS Total_Orders,
    ROUND(
        (SELECT COUNT(*) FROM orders WHERE Order_Status = 'Cancelled') * 100.0
        / (SELECT COUNT(*) FROM orders), 2
    ) AS Cancellation_Rate_Pct;

-- 11. Average delivery time overall and by city
SELECT City, ROUND(AVG(Delivery_Time_Minutes), 1) AS Avg_Delivery_Time_Min
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY City
ORDER BY Avg_Delivery_Time_Min DESC;

-- 12. Highest-rated restaurants (min 15 orders to avoid noisy small samples)
SELECT Restaurant_Name,
       COUNT(*) AS Orders,
       ROUND(AVG(Customer_Rating), 2) AS Avg_Rating
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Restaurant_Name
HAVING COUNT(*) >= 15
ORDER BY Avg_Rating DESC
LIMIT 10;

-- 13. Customers with highest spending, segmented via CASE
SELECT Customer_ID, Customer_Name,
       ROUND(SUM(Net_Revenue), 2) AS Total_Spend,
       CASE
           WHEN SUM(Net_Revenue) >= 5000 THEN 'High Value'
           WHEN SUM(Net_Revenue) >= 2000 THEN 'Medium Value'
           ELSE 'Low Value'
       END AS Customer_Segment
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Customer_ID, Customer_Name
ORDER BY Total_Spend DESC
LIMIT 20;

-- 14. Revenue generated through different payment methods
SELECT Payment_Method,
       COUNT(*) AS Orders,
       ROUND(SUM(Net_Revenue), 2) AS Revenue,
       ROUND(SUM(Net_Revenue) * 100.0 / (
           SELECT SUM(Net_Revenue) FROM orders WHERE Order_Status != 'Cancelled'
       ), 2) AS Pct_Of_Total_Revenue
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Payment_Method
ORDER BY Revenue DESC;

-- 15. Peak ordering hours
SELECT Order_Hour, COUNT(*) AS Orders
FROM orders
GROUP BY Order_Hour
ORDER BY Orders DESC;

-- 16. Weekday vs weekend order comparison
SELECT CASE WHEN Is_Weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS Day_Type,
       COUNT(*) AS Orders,
       ROUND(AVG(Net_Revenue), 2) AS Avg_Order_Value
FROM orders
WHERE Order_Status != 'Cancelled'
GROUP BY Is_Weekend;

-- 17. Restaurants with high cancellation rates (min 20 orders)
SELECT Restaurant_Name,
       COUNT(*) AS Total_Orders,
       SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled_Orders,
       ROUND(SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Cancellation_Rate_Pct
FROM orders
GROUP BY Restaurant_Name
HAVING COUNT(*) >= 20
ORDER BY Cancellation_Rate_Pct DESC
LIMIT 10;

-- 18. Distance vs delivery time correlation buckets (subquery + CASE)
SELECT Distance_Bucket,
       ROUND(AVG(Delivery_Time_Minutes), 1) AS Avg_Delivery_Time_Min,
       COUNT(*) AS Orders
FROM (
    SELECT *,
           CASE
               WHEN Distance_KM < 3 THEN '0-3 km'
               WHEN Distance_KM < 6 THEN '3-6 km'
               WHEN Distance_KM < 10 THEN '6-10 km'
               ELSE '10+ km'
           END AS Distance_Bucket
    FROM orders
    WHERE Order_Status != 'Cancelled'
)
GROUP BY Distance_Bucket
ORDER BY MIN(Distance_KM);

-- 19. New vs returning customers (customers with >1 order = returning)
SELECT
    CASE WHEN Order_Count > 1 THEN 'Returning' ELSE 'New (single order)' END AS Customer_Type,
    COUNT(*) AS Num_Customers,
    SUM(Order_Count) AS Total_Orders
FROM (
    SELECT Customer_ID, COUNT(*) AS Order_Count
    FROM orders
    WHERE Order_Status != 'Cancelled'
    GROUP BY Customer_ID
)
GROUP BY Customer_Type;

-- 20. Delayed-order percentage (delivery time > 45 min threshold)
SELECT
    SUM(CASE WHEN Is_Delayed = 1 THEN 1 ELSE 0 END) AS Delayed_Orders,
    COUNT(*) AS Total_Delivered_Orders,
    ROUND(SUM(CASE WHEN Is_Delayed = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Delayed_Pct
FROM orders
WHERE Order_Status != 'Cancelled';
