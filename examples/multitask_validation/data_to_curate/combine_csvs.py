import os
import pandas as pd
from sklearn.utils import shuffle

dir = "test"
dfs = []
for f in sorted(os.listdir(dir)):
    if ".csv" not in f:
        continue
    f = os.path.join(dir, f)
    df = pd.read_csv(f, header=None)
    dfs.append(df)
df = pd.concat(dfs)
df = shuffle(df)
df.to_csv("test_shuffled.csv", header=None)

