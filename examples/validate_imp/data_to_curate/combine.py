import pandas as pd
import os

dir = "batch1"
files = [f for f in os.listdir(dir) if "batch" in f]

dfs = []
for file in files:
    df = pd.read_csv(os.path.join(dir, file), sep="\t", header=None)
    dfs.append(df)

# df = pd.concat(dfs)
df = pd.concat(dfs).reset_index(drop=True)
df.to_csv("combined1.tsv", sep="\t", header=None)