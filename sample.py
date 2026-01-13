import pandas as pd

# paramètres
input_csv = "data/extrait_bdd_sirene.csv"
output_csv = "data/sample_sirene.csv"
n = 1000          # nombre de lignes à extraire
seed = 42         # pour reproductibilité (optionnel)

# lecture du CSV
df = pd.read_csv(input_csv, low_memory=False)

# échantillonnage aléatoire
sample_df = df.sample(n=n, random_state=seed)

# sauvegarde dans un nouveau CSV
sample_df.to_csv(output_csv, index=False)

