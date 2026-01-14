import pandas as pd

n = 1000
seed = 42

files = [
    ("data/extrait_bdd_sirene.csv", "data/sample_sirene.csv"),
    ("data/extrait_bdd_rne.csv", "data/sample_rne.csv"),
]

for input_csv, output_csv in files:
    df = pd.read_csv(input_csv, low_memory=False)
    sample_df = df.sample(n=n, random_state=seed)
    sample_df.to_csv(output_csv, index=False)
