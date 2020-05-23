# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=500, help='how many validate ordinary morality hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
# parser.add_argument('--num_samples', type=int, default=4, help='')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/results/combined.tsv", sep="\t", header=None)
# df = df[args.skip:args.skip + args.num_samples*args.hits]
df = df[args.skip:args.skip + args.hits]

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

df = shuffle(df)  # to avoid pairs in the same batch
list_of_dicts = []  # will save these dicts
for i in range(df.shape[0]):
    d = {}
    idx = df.iloc[i, 0]
    d["scenario"] = df.iloc[i, 1]
    reasonable = eval(df.iloc[i, 2])
    unreasonable = eval(df.iloc[i, 3])
    all_excuses = reasonable + unreasonable
    assert len(all_excuses) == 6

    # want to present in a random order.
    order = np.random.permutation(np.arange(6))

    for j in range(6):
        k = order[j]
        d["reasonable_{}".format(j)] = "reasonable_idx{}_k{}".format(idx, k)
        d["unreasonable_{}".format(j)] = "unreasonable_idx{}_k{}".format(idx, k)
        d["excuse{}".format(j)] = all_excuses[k]

    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

