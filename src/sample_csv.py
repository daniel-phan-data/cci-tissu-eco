import pandas as pd

input_csv = "data/extrait_bdd_sirene.csv"
output_csv = "data/sample_sirene.csv"
n = 1000
seed = 42

df = pd.read_csv(input_csv, low_memory=False)
sample_df = df.sample(n=n, random_state=seed)
sample_df.to_csv(output_csv, index=False)

