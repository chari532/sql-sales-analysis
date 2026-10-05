import pandas as pd
import sqlite3

df = pd.read_csv("SQL_Sales_Dataset.csv")

conn = sqlite3.connect("Sales_data.db")
df.to_sql("df",conn, if_exists="replace", index = False)

query_1 = '''SELECT * FROM df'''
query_2 = '''SELECT customer_name,category,product_name,quantity FROM df WHERE category == "Clothing" '''
query_3 = '''SELECT AVG(total_price) FROM (SELECT order_id, SUM(quantity * unit_price) AS total_price FROM df GROUP BY order_id)'''
query_4 = '''SELECT order_id, customer_name, SUM(quantity * unit_price) AS total_spent,
    CASE
        WHEN SUM(quantity * unit_price) >= 15000 THEN 'High Value'
        WHEN SUM(quantity * unit_price) BETWEEN 1000 AND 15000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_tier FROM df GROUP BY order_id, customer_name'''
query_5 = '''SELECT customer_name,SUM(quantity * unit_price) AS total_spent FROM df GROUP BY customer_name ORDER BY total_spent DESC LIMIT 10'''

df_all = pd.read_sql(query_1, conn)
df_clothing = pd.read_sql(query_2, conn)
df_aov = pd.read_sql(query_3, conn)
df_tiers = pd.read_sql(query_4, conn)
df_top_10 = pd.read_sql(query_5, conn)

conn.close()

print("--- TOP 10 CUSTOMERS ---")
print(df_top_10)

print(f"\n---AVERAGE ORDER VALUE: ${df_aov.iloc[0,0]:.2f} ---")
