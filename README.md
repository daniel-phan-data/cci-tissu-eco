# CCI group assignment

2 weeks group project for CCI Marnes Ardennes: find and analyze data to study the region's activity.

## Data

The data used has been provided by the CCI itself and won't be available on this repo.

## Recommandations/Instructions to run our scripts

1. Install **Python 3.13**: From [Python.org](https://www.python.org/).

2. Install **uv**: From [https://docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

3. Clone the Git repository to your local machine and move there:

```bash
git clone https://gitlab-mi.univ-reims.fr/phan0005/cci-tissu-eco.git sep-cci
cd sep-cci
```

1. Run any script you want with `uv run + path_to_file` like this (you need the data and modify the paths in the code accordingly):

```bash
uv run src/convert_to_sql.py
```

## Scripts description

- convert_csv_to_sql.py: convert the 2 csv provided by the CCI into a SQLite database to allow SQL queries and better performance, on top of merging also creates 2 tables localisation and lifecycle for very specific analysis
- sample_csv.py: helper script to sample large csvs and allow quick tests
- sql_query_example: example code snipper to perform SQL queries on our database

## Authors

- Asma ZOULIM
- Kim Ngan THAI
- Rezi SABASHVILI
- Daniel PHAN
