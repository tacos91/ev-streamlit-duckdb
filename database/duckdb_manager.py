import duckdb
import pandas as pd

DB_PATH = "ev_data.duckdb"

def get_connection():
    return duckdb.connect(DB_PATH)

def store_dataframe(df: pd.DataFrame, table_name: str = "ev_data"):
    con = get_connection()
    con.execute(f"DROP TABLE IF EXISTS {table_name}")
    con.register("df_view", df)
    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_view")
    con.close()
