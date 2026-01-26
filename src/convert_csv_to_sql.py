"""
script to turn the 2 initial csv (given by cci) in a db file with 3 tables
core: just a simple fusion
lifecycle: beginning and end of activities
localisation: geographical data
"""

import sqlite3
import pandas as pd

CSV_RNE: str = "data/extrait_bdd_rne.csv"
CSV_SIRENE: str = "data/extrait_bdd_sirene.csv"
DB_PATH: str = "data/entreprises.db"

conn = sqlite3.connect(DB_PATH)

# df_rne: pd.DataFrame = pd.read_csv(CSV_RNE)
# df_sirene: pd.DataFrame = pd.read_csv(CSV_SIRENE)

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """clean column names of a pandas dataframe"""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(" ", "_")
    )
    return df

df_rne = clean_columns(
    pd.read_csv(CSV_RNE)
)
df_sirene = clean_columns(
    pd.read_csv(CSV_SIRENE)
)

# TABLE 1 : entreprises_core (simple merge of the 2 csv)

df_core = df_sirene.merge(
    df_rne[["siren", "type_entreprise"]],
    on="siren",
    how="left"
)

df_core = df_core[
    [
        "siren",
        "raison_sociale",
        "forme_juridique",
        "code_ape",
        "date_creation",
        "categorie_entreprise",
        "etat_administratif",
        "tranche_effectif",
        "type_entreprise",
    ]
]

df_core.to_sql(
    "entreprises_core",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "siren": "TEXT",
        "forme_juridique": "INTEGER",
        "code_ape": "TEXT",
        "date_creation": "DATE",
        "etat_administratif": "TEXT",
    },
)

# TABLE 2 : entreprises_lifecycle

df_lifecycle = df_rne[
    [
        "siren",
        "date_debutactivite",
        "date_cessationtotaleactivite",
        "date_radiation",
        "date_liquidation",
    ]
]

df_lifecycle.to_sql(
    "entreprises_lifecycle",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "siren": "TEXT",
        "date_debutactivite": "DATE",
        "date_cessationtotaleactivite": "DATE",
        "date_radiation": "DATE",
        "date_liquidation": "DATE",
    },
)

# TABLE 3 : entreprises_localisation

df_localisation = df_rne[
    ["siren", "commune", "code_postal", "nro_voie", "voie"]
]

df_localisation.to_sql(
    "entreprises_localisation",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "siren": "TEXT",
        "code_postal": "TEXT",
    },
)

# indexing for performance

cursor = conn.cursor()

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_core_siren ON entreprises_core(siren)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_lifecycle_siren ON entreprises_lifecycle(siren)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_localisation_siren ON entreprises_localisation(siren)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_core_code_ape ON entreprises_core(code_ape)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_localisation_commune ON entreprises_localisation(commune)"
)

conn.commit()
conn.close()

print("SQLite db successfully created", DB_PATH)
