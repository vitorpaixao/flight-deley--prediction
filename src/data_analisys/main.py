import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

airports = pd.read_csv("data/airports.csv")

print(airports)
print(f"Total rows: {len(airports)}")

airports.dropna(inplace=True)

print(f"Total after DropNA rows: {len(airports)}")