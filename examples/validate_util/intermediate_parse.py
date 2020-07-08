import os
import argparse
import json
import numpy as np
import pickle
import pandas as pd

dir = "arxiv_batches"
batch_files = [f for f in os.listdir(dir)]
json_files = [os.path.join(batch_file, "saved_data.jsonl") for batch_file in batch_files]

bad_workers = []
with open("bad_workers.txt", "r") as f:
    tmp = f.readlines()
    bad_workers = [line.strip() for line in tmp]
# print(bad_workers)

extra_bad_workers = []

dfs = []
good_idxs = []
for json_file in json_files:
    with open(os.path.join(dir, json_file), "r") as f:
        tmp = f.readlines()
        data = [json.loads(line.strip()) for line in tmp]
        
    results = {}
    # df = pd.read_csv("data_to_curate/nonmanual_cleaning_util.tsv", sep="\t", header=None)
    df = pd.read_csv("data_to_curate/arxiv_combined.tsv", sep="\t", header=None)

    KEY = {"ex1_better": -1, "unclear": 0, "ex2_better": 1}

    worker_answers = {}

    for d in data:
        answers = eval(d["taskAnswers"].replace("false", "False").replace("true", "True"))[0]
        worker = d["WorkerId"]
        if worker in bad_workers:
            continue

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

            if worker in worker_answers.keys():
                worker_answers[worker].append(ans)
            else:
                worker_answers[worker] = [ans]

    results_by_idx = []
    for idx in results:
        r = results[idx]
        if len(r) >= 4:
            good_idxs.append(idx)

    idxs = [idx for idx in results]
    idxs = np.sort(idxs)
    s1s = [df.iloc[idx, 0] for idx in idxs]
    s2s = [df.iloc[idx, 1] for idx in idxs]
    labels = [results[idx] for idx in idxs]

    df = pd.DataFrame({"idxs": idxs, "s1": s1s, "s2": s2s, "labels": labels})
    save_name = json_file.split("/")[-2] + "_arxiv.tsv"
    dfs.append(df)

    for worker in worker_answers.keys():
        if len(worker_answers[worker]) > 50 and np.mean(worker_answers[worker]) > -0.4:
            # print(worker, len(worker_answers[worker]), np.mean(worker_answers[worker]))
            extra_bad_workers.append(worker)

df = pd.concat(dfs)
df = df.sort_values("idxs")
good_idxs.sort()
print(df)
orig_df = pd.read_csv("data_to_curate/arxiv_combined.tsv", sep="\t", header=None)
n = orig_df.shape[0]
bad_idxs = [idx for idx in range(n) if idx not in good_idxs]
with open("bad_idxs.txt", "w") as f:
    for idx in bad_idxs:
        f.write("{}\n".format(idx))
if len(extra_bad_workers) > 0:
    print("additional bad workers", extra_bad_workers)
