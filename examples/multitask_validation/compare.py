import numpy as np
import os
import pandas as pd

batches = [f for f in os.listdir(".") if "batch-" in f]
df = pd.concat([pd.read_csv(f, sep="\t", header=None) for f in batches])
df = df.sort_values(0)
print(df)

india_labels = {}
india_labels_mean = {}
for i in range(df.shape[0]):
    idx = int(df.iloc[i, 0])
    # skip idx 0 (scenario = "input") and subtract one from the rest
    if idx == 0:
        continue
    idx -= 1
    if np.mean(eval(df.iloc[i, 1])) == 0.5:
        res = np.random.random() > 0.5
    else:
        res = int(np.mean(eval(df.iloc[i, 1])) > 0.5)
    india_labels[idx] = res
    india_labels_mean[idx] = np.mean(eval(df.iloc[i, 1]))

data = pd.read_csv("data_to_curate/cm_val_short.tsv", sep="\t")

eq = []
non_eq_idxs = []
for idx in india_labels.keys():
    if idx == 0:
        continue  # error
    print(idx, data.shape)
    label = data.iloc[idx, 0]
    india_label = india_labels[idx]
    eq.append(india_label == label)
    if india_label != label:
        non_eq_idxs.append(idx)

print(np.mean(eq))

# now print some of the disagreements
with open("indian_disagreements.txt", "w") as f:
    for idx in non_eq_idxs:
        sc = data.iloc[idx, 1]
        label_mean = india_labels_mean[idx]
        # print(label_mean, sc)
        f.write("{}: {}\n".format(label_mean, sc))

