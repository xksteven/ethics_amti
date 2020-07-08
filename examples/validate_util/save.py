import argparse
import json
import numpy as np
import pickle
import pandas as pd
import os

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

dirs = [f for f in os.listdir(".") if "batch-" in f]
print("dirs", dirs)

good_idxs = []

for dir in dirs:
    file = os.path.join(dir, "saved_data.jsonl")

    with open(file, "r") as f:
        tmp = f.readlines()
        data = [json.loads(line.strip()) for line in tmp]

    results = {}
    df = pd.read_csv("data_to_curate/nonmanual_cleaning_util.tsv", sep="\t", header=None)

    KEY = {"ex1_better": -1, "unclear": 0, "ex2_better": 1}

    for d in data:
        answers = eval(d["taskAnswers"].replace("false", "False").replace("true", "True"))[0]
        for key_num, key in enumerate(answers.keys()):
            idx = int(key.split("_")[0][3:])
            j = int(key.split("_")[1][1:])

            # get answer
            subdict = answers[key]
            # print("subdict", subdict)
            if "unclear" in subdict and True in subdict.values():  # only one item
                ans = KEY["unclear"]
            elif "ex1" in key and True in subdict.values():
                ans = KEY["ex1_better"]
            elif "ex2" in key and True in subdict.values():
                ans = KEY["ex2_better"]
            else:
                continue

            if (idx, j) in results.keys():
                results[(idx, j)].append(ans)
            else:
                results[(idx, j)] = [ans]

    for idx in range(10000):
        good = True
        r = []
        lengths, sums = [], []
        for j in range(4):
            key = (idx, j)
            # assert key in results
            if key not in results:
                break
            r += results[key]
            lengths += [len(results[key])]
            sums += [np.sum(results[key])]
            if np.sum(np.array(results[key])) >= 0:
            # if np.sum(results[key]) > -2:
            # if np.sum(results[key] == -1) < 2:
                good = False
        if key not in results:
            continue
        print(idx, lengths, sums)
        for j in range(5):
            print(df.iloc[idx, j])

        if good:
            good_idxs.append(idx)

    # print(results)
print(good_idxs)
print(len(good_idxs))

s1s = [df.iloc[idx, 0] for idx in good_idxs]
s2s = [df.iloc[idx, 1] for idx in good_idxs]
s3s = [df.iloc[idx, 2] for idx in good_idxs]
s4s = [df.iloc[idx, 3] for idx in good_idxs]
s5s = [df.iloc[idx, 4] for idx in good_idxs]
workers = [df.iloc[idx, 5] for idx in good_idxs]
df = pd.DataFrame({"s1": s1s, "s2": s2s, "s3": s3s, "s4": s4s, "s5": s5s, "workers": workers})
print(len(df))
df.to_csv("nonmanual_cleaned_util.tsv", sep="\t", header=None, index=None)
#print(df)

