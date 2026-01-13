import sqlite3
import pandas as pd

DB_PATH = "data/entreprises.db"
n = 10  # nombre de lignes à afficher

conn = sqlite3.connect(DB_PATH)

query = f"""
SELECT *
FROM entreprises_lifecycle
LIMIT {n};
"""

df = pd.read_sql(query, conn)
# print(df)
print(df.reset_index(drop=True))


conn.close()
