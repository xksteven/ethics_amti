import os
import numpy as np
import pandas as pd

to_clean = ["old_mturk_first_person", "remaining_first_person"]
dir = "data_to_curate"
delta = 0.21

dfs = []
all_scenarios = []
all_labels = []
for c in to_clean:
    file = os.path.join(dir, c + ".tsv")
    df = pd.read_csv(file, sep="\t", header=None)
    print(df.shape)

    cdir = c + "_results"
    batches = os.listdir(cdir)

    good_labels = {}
    for bfile in batches:
        print("bfile", bfile)
        bdf = pd.read_csv(os.path.join(cdir, bfile), sep="\t", header=None)
        print(bdf.shape)

        for i in range(bdf.shape[0]):
            idx = bdf.iloc[i, 0]
            scenario = df.iloc[idx, df.shape[1]-1]
            labels = eval(bdf.iloc[i, 1])

            if np.mean(labels) > 1-delta:
                all_scenarios.append(scenario)
                all_labels.append(1)
                good_labels[idx] = 1
            elif np.mean(labels) < delta:
                good_labels[idx] = 0
                all_scenarios.append(scenario)
                all_labels.append(0)
                
    print(len(good_labels))

    """
    all_scenarios, all_labels = [], []
    for i in range(bdf.shape[0]):
        idx = bdf.iloc[i, 0]
        if idx in good_labels:
            all_scenarios.append(df.iloc[idx, 1])
            all_labels.append(good_labels[idx])
    cleaned_df = pd.DataFrame({"labels": all_labels, "scenarios": all_scenarios})
    dfs.append(cleaned_df)
    print(cleaned_df)
    """

#df = pd.concat(dfs)
df = pd.DataFrame({"labels": all_labels, "scenarios": all_scenarios})
print(df)
print(df.shape)
df.to_csv("short_om_neurips.tsv", sep="\t", header=None, index=None)

