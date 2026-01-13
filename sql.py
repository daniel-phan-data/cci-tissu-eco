import sqlite3
import pandas as pd

# =========================
# PARAMÈTRES
# =========================

CSV_RNE = "data/sample_rne.csv"
CSV_SIRENE = "data/sample_sirene.csv"
DB_PATH = "data/entreprises.db"

# =========================
# CONNEXION SQLITE
# =========================

conn = sqlite3.connect(DB_PATH)

# =========================
# LECTURE DES CSV
# =========================

df_rne = pd.read_csv(CSV_RNE)
df_sirene = pd.read_csv(CSV_SIRENE)

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(" ", "_")
    )
    return df

df_rne = clean_columns(df_rne)
df_sirene = clean_columns(df_sirene)

# =========================
# TABLE 1 : entreprises_core
# =========================
# Base SIRENE + enrichissement RNE

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

# =========================
# TABLE 2 : entreprises_lifecycle
# =========================

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

# =========================
# TABLE 3 : entreprises_localisation
# =========================

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

# =========================
# INDEX (PERFORMANCE)
# =========================

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

print("Base SQLite créée avec succès :", DB_PATH)

print(df_rne.columns.tolist())
print(df_sirene.columns.tolist())

