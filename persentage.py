import pandas as pd

df = pd.read_csv("marks/41110378.csv")

print(df["Total"].sum() / 9)