import argparse
import json
import numpy as np
import pickle
import pandas as pd

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

with open(args.json, "r") as f:
    tmp = f.readlines()
    data = [json.loads(line.strip()) for line in tmp]

results = {}
# df = pd.read_csv("data_to_curate/nonmanual_cleaning_util.tsv", sep="\t", header=None)
df = pd.read_csv("data_to_curate/arxiv_combined.tsv", sep="\t", header=None)

KEY = {"ex1_better": -1, "unclear": 0, "ex2_better": 1}

for d in data:
    answers = eval(d["taskAnswers"].replace("false", "False").replace("true", "True"))[0]
    # print(answers)
    for key_num, key in enumerate(answers.keys()):
        # print(key_num, key)
        idx = int(key.split("_")[0][3:])
        # print(idx)

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

        if idx in results.keys():
            results[idx].append(ans)
        else:
            results[idx] = [ans]

results_by_idx = []
good_idxs = []
for idx in results:
    r = results[idx]
    if np.sum(results[idx]) <= -2:
        good_idxs.append(idx)

# print(results)
print(good_idxs)

# s1s = [df.iloc[idx, 0] for idx in good_idxs]
# s2s = [df.iloc[idx, 1] for idx in good_idxs]
idxs = [idx for idx in results]
idxs = np.sort(idxs)
s1s = [df.iloc[idx, 0] for idx in idxs]
s2s = [df.iloc[idx, 1] for idx in idxs]
labels = [results[idx] for idx in idxs]
# workers = [df.iloc[idx, 2] for idx in good_idxs]
# df = pd.DataFrame({"s1": s1s, "s2": s2s, "workers": workers})
# df = pd.DataFrame({"s1": s1s, "s2": s2s})
df = pd.DataFrame({"idxs": idxs, "s1": s1s, "s2": s2s, "labels": labels})
print(len(df))
save_name = args.json.split("/")[-2] + "_arxiv.tsv"
# df.to_csv("arxiv_extra_nonexpert_cleaned_util.tsv", sep="\t", header=None, index=None)
df.to_csv(save_name, sep="\t", header=None, index=None)
