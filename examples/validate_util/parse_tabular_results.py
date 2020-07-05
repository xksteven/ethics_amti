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

good_idxs = []
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
