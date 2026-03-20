import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

flights = pd.read_csv("data/flights.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(flights.head(15))
print(f"Total rows: {len(flights)}")

flights.dropna(inplace=True)

print(f"Total after DropNA rows: {len(flights)}")