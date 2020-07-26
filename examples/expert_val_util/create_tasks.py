# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=100, help='how many hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=4, help='number of samples used per hit')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/arxiv_test_to_clean.tsv", sep="\t", header=None)
# df = pd.read_csv("data_to_curate/arxiv_val_to_clean.tsv", sep="\t", header=None)

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

# df = shuffle(df)  # to avoid pairs in the same batch
list_of_dicts = []  # will save these dicts
print(df)

for hit_num in range(args.hits):
    start_idx = args.skip + args.num_samples*hit_num
    d = {}
    for j in range(args.num_samples):
        idx = start_idx + j
        is_swapped = "is_swapped" if np.random.random() < 0.5 else "not_swapped"
        d["first_{}".format(j)] = "first_{}_{}".format(idx, is_swapped)
        d["second_{}".format(j)] = "second_{}_{}".format(idx, is_swapped)
        d["low_quality_{}".format(j)] = "low_quality_{}_{}".format(idx, is_swapped)
        sc0, sc1 = df.iloc[idx, 0].replace("\"", "\'"), df.iloc[idx, 1].replace("\"", "\'")

        if is_swapped == "is_swapped":
            d["sent{}0".format(j)] = sc1
            d["sent{}1".format(j)] = sc0
        else:
            d["sent{}0".format(j)] = sc0
            d["sent{}1".format(j)] = sc1

    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

