import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "data/pokedex.sqlite"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
df = pd.read_csv("data/pokedex.csv")

df.to_sql(name="pokedex", con=engine, index=False)
