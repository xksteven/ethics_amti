# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=100, help='how many validate ordinary morality hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=4, help='')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/old_mturk_first_person.tsv", sep="\t", header=None)
df = df[args.skip:args.skip + args.num_samples*args.hits]

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

df = shuffle(df)  # to avoid pairs in the same batch
list_of_dicts = []  # will save these dicts
for i in range(df.shape[0] // args.num_samples):
    d = {}
    for j in range(args.num_samples):
        idx = df.index[i*args.num_samples+j] + args.skip
        d["scenario{}".format(j)] = df.iloc[i*args.num_samples + j, 1]
        d["good_{}".format(j)] = "good_idx{}".format(idx+args.skip)
        d["bad_{}".format(j)] = "bad_idx{}".format(idx+args.skip)

    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

