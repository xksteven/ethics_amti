# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=100, help='how many hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=10, help='number of samples used per hit')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/test_justice_arxiv.tsv", sep="\t", header=None)
df = df[args.skip:args.skip + args.num_samples*args.hits]
# df = df[args.skip:args.skip + args.hits]

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
        sc = df.iloc[idx, 1]
        d["sent{}".format(j)] = sc
        d["good_{}".format(j)] = "good_{}".format(idx)
        d["bad_{}".format(j)] = "bad_{}".format(idx)
        d["low_quality_{}".format(j)] = "low_quality_{}".format(idx)

    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

