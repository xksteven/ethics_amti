# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--batch_size', '-b', type=int, default=400, help='how many extra ob hits to submit')
parser.add_argument('--skip', '-s', type=int, default=0)
args = parser.parse_args()

df = pd.read_csv("data_to_curate/ob.tsv", sep="\t", header=None)
begin = args.skip
end = args.skip + args.batch_size
df = df[begin:end]

savefile = "data.jsonl"


class mydict(dict):
    def __str__(self):
        return json.dumps(self)

list_of_dicts = []  # will save these dicts
for i in range(df.shape[0]):
    s = df.iloc[i, 0]
    id = df.iloc[i, -1]
    idx = begin + i
    v = "idx{:04d}".format(idx)
    d = mydict({"scenario": s, "v1": "{}_1".format(v), "v2": "{}_2".format(v)})
    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(d))

