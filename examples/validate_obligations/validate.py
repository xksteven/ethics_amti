import pandas as pd
import os
import numpy as np

new = True
if new:
    dir = "new_results"
    file = "new_combined.tsv"
else:
    dir = "results"
    file = "combined.tsv"
# val_files = [f for f in os.listdir(dir) if "batch" in f]
val_files = os.listdir(dir)
print(val_files)

df = pd.read_csv(os.path.join("data_to_curate", dir, file), sep="\t", header=None)
print(df)

idxs = []
ks = []
reasonables = []
scenarios = []
excuses = []

for file in val_files:
    val_df = pd.read_csv(os.path.join(dir, file), sep="\t", header=None)
    # print(val_df)
    for j in range(val_df.shape[0]):
        idx, k, labels = val_df.iloc[j, 0], val_df.iloc[j, 1], eval(val_df.iloc[j, 2])
        labels = np.array(labels)
        scenario = df.iloc[idx, 1]
        excuse = eval(df.iloc[idx, 2]) + eval(df.iloc[idx, 3])
        excuse = excuse[k]

        # if labels.mean() > 0.79:
        if labels.mean() > 0.99:
            idxs.append(idx)
            reasonables.append(True)
            scenarios.append(scenario)
            excuses.append(excuse)
            ks.append(k)
            # if labels.mean() < 0.99:
            #     print(scenario, excuse, True)
        # elif labels.mean() < 0.19:
        elif labels.mean() < 0.01:
            idxs.append(idx)
            scenarios.append(scenario)
            excuses.append(excuse)
            ks.append(k)
            reasonables.append(False)
            # if labels.mean() > 0.01:
            #     print(scenario, excuse, False)

print(len(idxs), len(ks), len(reasonables), len(scenarios), len(excuses))
df = pd.DataFrame({"idxs": idxs, "ks": ks, "reasonable": reasonables, "scenario": scenarios, "excuse": excuses})
print(df)
print(df.shape)
if new:
    df.to_csv("new_validated_ob.tsv", sep="\t", header=None)
else:
    df.to_csv("validated_ob.tsv", sep="\t", header=None)

# TODO: find and delete repetitions
