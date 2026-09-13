import sqlite3
from pathlib import Path

import pandas as pd

DB = Path("data/prices.db")
SQL_DIR = Path("sql")


def run(sql_file, db_path=DB):
    """Execute a .sql file against the database, return a DataFrame."""
    query = Path(sql_file).read_text(encoding="utf-8").strip()
    if not query:
        raise ValueError(f"{sql_file} is empty — did you save it?")
    con = sqlite3.connect(db_path)
    result = pd.read_sql_query(query, con)
    con.close()
    return result

if __name__ == "__main__":
    for path in sorted(SQL_DIR.glob("*.sql")):
        print(f"\n===== {path.name} =====")
        print(run(path).to_string(index=False))