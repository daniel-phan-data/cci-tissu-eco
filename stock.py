import pandas as pd
import sqlite3

# 1. Load CSV
csv_file = "data/sample_unite_legale.csv"  # Replace with your CSV path
df = pd.read_csv(csv_file, sep=",", dtype=str)  # Read all columns as string to avoid type issues

# Optional: Replace '[ND]' with None for missing values
df.replace("[ND]", None, inplace=True)

# 2. Connect to SQLite (creates file if not exists)
db_file = "data/sample_unite_legale.db"
conn = sqlite3.connect(db_file)

# 3. Write dataframe to SQLite table
df.to_sql("siren", conn, if_exists="replace", index=False)

# 4. Close connection
conn.close()

print(f"Database created successfully: {db_file}")


# naf_df = pd.read_csv("nomenclature_naf.csv", dtype=str)  # columns: code, description
# merged = df.merge(naf_df, left_on="activitePrincipaleUniteLegale", right_on="code", how="left")

