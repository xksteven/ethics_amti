# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=100, help='how many validate ordinary morality hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=8, help='')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/combined1.tsv", sep="\t", header=None)
df = df[args.skip:args.skip + args.num_samples*args.hits]
# df = df[args.skip:args.skip + args.hits]

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

df = shuffle(df)  # to avoid pairs in the same batch
list_of_dicts = []  # will save these dicts
for i in range(args.hits):
    d = {}
    for k in range(args.num_samples):
        index = args.num_samples*i + k

        scenario_idx = df.iloc[index, 1]
        j = df.iloc[index, 2]
        scenario = df.iloc[index, 3]
        # print(scenario_idx)
        # print(j)
        # print(scenario)
        d["scenario{}".format(k)] = scenario
        d["reasonable_{}".format(k)] = "reasonable_scenario_idx{}_j{}".format(scenario_idx, j)
        d["unreasonable_{}".format(k)] = "unreasonable_scenario_idx{}_j{}".format(scenario_idx, j)

    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

