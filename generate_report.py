import sqlite3
import pandas as pd

conn = sqlite3.connect("Sales.db")
print("Extracting analytics dataframes...")

q1 = "SELECT * FROM df"
q2 = "SELECT customer_name, category, product_name, quantity FROM df WHERE category = 'Clothing'"
q3 = "SELECT AVG(total_price) AS global_aov FROM (SELECT order_id, SUM(quantity * unit_price) AS total_price FROM df GROUP BY order_id)"
q4 = "SELECT order_id, customer_name, SUM(quantity * unit_price) AS total_spent, CASE WHEN SUM(quantity * unit_price)  THEN 'High Value' WHEN SUM(quantity * unit_price) BETWEEN 1000 AND 15000 THEN 'Medium Value' ELSE 'Low Value' END AS customer_tier FROM df GROUP BY order_id, customer_name"
q5 = "SELECT customer_name, SUM(quantity * unit_price) AS total_spent FROM df GROUP BY customer_name ORDER BY total_spent DESC LIMIT 10"

df_all = pd.read_sql_query(q1, conn)
df_clothing = pd.read_sql_query(q2, conn)
df_aov = pd.read_sql_query(q3, conn)
df_tiers = pd.read_sql_query(q4, conn)
df_top_10 = pd.read_sql_query(q5, conn)

print("Generating multi-tab Excel Workbook...")
with pd.ExcelWriter("Sales_Analysis_Report.xlsx", engine="openpyxl") as writer:
    df_all.to_excel(writer, sheet_name="Raw Data Preview", index=False)
    df_clothing.to_excel(writer, sheet_name="Clothing Segment", index=False)
    df_aov.to_excel(writer, sheet_name="Global AOV Metrics", index=False)
    df_tiers.to_excel(writer, sheet_name="Customer Value Tiers", index=False)
    df_top_10.to_excel(writer, sheet_name="Top 10 Customers", index=False)

conn.close()
print("SUCCESS: Automated Excel sheet generated as 'Sales_Analysis_Report.xlsx'!")
