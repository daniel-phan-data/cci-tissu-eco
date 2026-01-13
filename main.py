import pandas as pd

def main():
    print("Hello from cci!")


if __name__ == "__main__":
    main()
    # df: pd.DataFrame = pd.read_csv("data/extrait_bdd_rne(in).csv")
    df: pd.DataFrame = pd.read_csv("data/extrait_bdd_sirene.csv", low_memory=False)
    print(df.describe())

