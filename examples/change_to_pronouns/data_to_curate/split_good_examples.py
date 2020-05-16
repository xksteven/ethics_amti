import pandas as pd
import numpy as np

df = pd.read_csv("mturk_data.csv", sep="\t", names=["label", "text", "worker", "hit"])

mask1 = df["text"].str.count("I ") > 0
mask2 = df["text"].str.count(" i ") > 0
mask3 = df["text"].str.count(" me ") > 0
mask4 = df["text"].str.count(" my ") > 0
mask = mask1 | mask2 | mask3 | mask4
print(mask.mean())

df_good = df[mask]
df_bad = df[~mask]

df_good.to_csv("mturk_data_good.csv", sep="\t", index=None, header=None)
df_bad.to_csv("mturk_data_bad.csv", sep="\t", index=None, header=None)
