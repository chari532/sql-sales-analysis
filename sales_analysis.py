import sqlite3
import pandas as pd

df = pd.read_csv("SQL_Sales_Dataset.csv")
conn = sqlite3.connect("Sales.db")
df.to_sql("df", conn, if_exists="replace", index=False)

query_1 = "SELECT * FROM df LIMIT 5"
df_res = pd.read_sql_query(query_1, conn)
print(df_res)
conn.close()
