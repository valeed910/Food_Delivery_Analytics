# Business Insights & Recommendations
### Food Delivery Data Analytics and Business Intelligence Dashboard

Analysis period: **Jan 2024 – Dec 2025** | Dataset: 9,000 cleaned orders across 10 cities, 220 restaurants, 1,800 customers

---

## Executive Summary

| KPI | Value |
|---|---|
| Total Revenue (delivered orders) | ₹60,15,734 |
| Total Orders | 9,000 |
| Average Order Value | ₹742 |
| Cancellation Rate | 9.93% |
| Average Delivery Time | 24.8 minutes |
| Average Customer Rating | 3.95 / 5 |
| Delayed Orders (>45 min) | 6.55% |

---

## 1. What happened? (Observations)

### Sales
- **Kolkata (₹6.78L), Jaipur (₹6.72L), and Delhi (₹6.66L)** are the top three cities by revenue — the spread between the top and bottom cities is relatively narrow, indicating even geographic demand rather than one dominant market.
- **North Indian (₹7.31L), Biryani (₹7.05L), and Healthy (₹6.71L)** are the top-grossing food categories.
- The single top restaurant by revenue is **Saxena Diner (₹57,380)**, followed by Gole Kitchen and Deo Kitchen — no single restaurant dominates total revenue, meaning the business isn't overexposed to one partner.
- Weekend average order value (**₹749**) is marginally higher than weekday (**₹740**), and weekend orders make up ~29% of total order volume despite weekends being only 2/7 of the week — weekend demand per day is disproportionately high.

### Customers
- **1,688 of 1,784 active customers (94.6%) are returning customers**, and only 96 placed a single order — retention is strong.
- The **top 20% of customers generate 37.3% of total revenue** — a meaningful but not extreme concentration, suggesting a healthy customer base rather than dependence on a small VIP segment.

### Restaurants
- Restaurant revenue is broadly distributed; the top 10 restaurants together account for a modest share of total revenue, consistent with a long-tail restaurant marketplace.
- A small group of restaurants — **Patla Cafe (25.0%), Garde-Bhatt Kitchen (24.1%), Zacharia Inc Cafe (23.7%)** — show cancellation rates 2–2.5x the platform average of ~9.9%, among restaurants with at least 20 orders.

### Delivery
- **Distance and delivery time are strongly correlated (r = 0.73)** — delivery time scales predictably with distance, confirming distance is the primary driver of delivery duration rather than random operational variance.
- **Jaipur (7.75%), Hyderabad (7.10%), and Mumbai (6.64%)** have the highest delayed-order rates (>45 minutes), each above the platform-wide 6.55% average.

### Orders
- Ordering is strongly **bimodal**: a lunch peak around **12:00–13:00** and a much larger dinner peak around **19:00–21:00**, with 19:00–21:00 alone accounting for over 40% of daily order volume.
- Cancellation rate stands at **9.93%** of all orders — a level worth monitoring, particularly given it's concentrated in specific restaurants (see above).

---

## 2. Why did it happen? / What does the data tell us?

- The **strong distance–delivery-time correlation** indicates delivery delays are largely structural (geography/fleet allocation) rather than random restaurant-side inefficiency — this points toward a logistics/routing fix rather than a restaurant-training fix.
- **Concentrated cancellations in a handful of restaurants** (rather than being evenly spread) suggests restaurant-specific operational issues — such as inventory stock-outs or kitchen capacity — rather than a platform-wide problem.
- The **pronounced dinner peak** suggests demand is driven by habitual daily ordering (dinner replacement) more than occasional treat-ordering, which has implications for delivery-fleet scheduling and restaurant kitchen staffing.
- **High customer retention (94.6% returning)** combined with only moderate revenue concentration (top 20% = 37.3%) suggests the platform has broad, sustained engagement rather than reliance on a few big spenders — a healthier growth profile.

---

## 3. Business Recommendations

1. **Increase delivery-fleet allocation during 19:00–21:00**, the dominant dinner peak, to reduce delay risk during the highest-demand window — this is where the delayed-order percentage is likely concentrated.
2. **Investigate the restaurants with cancellation rates above ~20%** (Patla Cafe, Garde-Bhatt Kitchen, Zacharia Inc Cafe, Saraf-Kapadia House, Gupta Express) for stock, staffing, or order-acceptance issues before they erode customer trust.
3. **Prioritize delivery-routing improvements in Jaipur, Hyderabad, and Mumbai**, the three cities with the highest delayed-order rates, since distance is the dominant driver of delivery time — better zone-based rider allocation should have a direct, measurable effect.
4. **Promote North Indian, Biryani, and Healthy categories** in marketing and app placement, as they already lead in revenue and are well-positioned for further growth through bundling or featured placement.
5. **Introduce a loyalty tier for the top 20% of customers** (currently generating 37.3% of revenue) to protect and grow this segment, while running targeted reactivation offers for the 96 single-order customers to convert them into repeat buyers.
6. **Test lunch-hour promotions (12:00–13:00)** to grow the smaller of the two demand peaks, smoothing overall daily volume and improving asset utilization outside the dinner rush.
7. **Maintain the ~9.9% platform cancellation rate as a KPI to reduce**, with restaurant-level dashboards (Power BI Page 4) used to flag any restaurant crossing a 15% threshold for account-management follow-up.

---

## Note on Methodology

All figures are computed from the cleaned dataset (`data/cleaned_data.csv`, 9,000 rows) after
removing duplicates, correcting invalid values, and standardizing categorical fields —
see `reports/data_cleaning_log.txt` for the full cleaning log and
`notebooks/food_delivery_analysis.ipynb` for the complete analysis with charts.
Revenue and delivery-time metrics exclude cancelled orders unless stated otherwise,
since cancelled orders are never delivered or rated.
