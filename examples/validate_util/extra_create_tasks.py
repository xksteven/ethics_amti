# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--nhits', '-n', type=int, default=300)
parser.add_argument('--nsamples', '-m', type=int, default=8)  # per batch
parser.add_argument('--start', '-s', type=int, default=0)  
args = parser.parse_args()

# assert args.nhits % args.nsamples == 0
# assert args.nhits % 4 == 0

filename = "arxiv_combined.tsv"
df = pd.read_csv("data_to_curate/{}".format(filename), sep="\t", header=None)
#begin, end = args.start, args.start + args.nhits*args.nsamples
#df = df[begin:end]

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)


list_of_dicts = []  # will save these dicts
print("Number of examples to be cleaned:")
print(args.nsamples * args.nhits)
for i in range(args.nhits):
    d = {}
    for k in range(args.nsamples):
        idx = args.start + args.nsamples*i + k
        s1, s2 = df.iloc[idx, 0], df.iloc[idx, 1]  # s1 is more pleasant than s2

        # half the time swap the order
        if np.random.random() < 0.5:
            # new_d = {"left{}".format(k): s1, "right{}".format(k): s2, "idx{}".format(k): str(idx), "swapped{}".format(k): "false", "v0_{}".format(k): "idx{:04d}_j{}_ex1".format(idx, j), "v1_{}".format(k): "idx{:04d}_j{}_ex2".format(idx, j+1), "v2_{}".format(k): "idx{:04d}_j{}_j{}_amb".format(idx, j, j+1)}
            new_d = {"filename": filename, "left{}".format(k): s1, "right{}".format(k): s2, "idx{}".format(k): str(idx), "swapped{}".format(k): "false", "v0_{}".format(k): "idx{:04d}_ex1".format(idx), "v1_{}".format(k): "idx{:04d}_ex2".format(idx), "v2_{}".format(k): "idx{:04d}_amb".format(idx)}
        else:
            # new_d = {"left{}".format(k): s2, "right{}".format(k): s1, "idx{}".format(k): str(idx), "swapped{}".format(k): "true", "v0_{}".format(k): "idx{:04d}_j{}_ex2".format(idx, j+1), "v1_{}".format(k): "idx{:04d}_j{}_ex1".format(idx, j), "v2_{}".format(k): "idx{:04d}_j{}_j{}_amb".format(idx, j, j+1)}
            new_d = {"filename": filename, "left{}".format(k): s2, "right{}".format(k): s1, "idx{}".format(k): str(idx), "swapped{}".format(k): "true", "v0_{}".format(k): "idx{:04d}_ex2".format(idx), "v1_{}".format(k): "idx{:04d}_ex1".format(idx), "v2_{}".format(k): "idx{:04d}_amb".format(idx)}

        d.update(new_d)
    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

