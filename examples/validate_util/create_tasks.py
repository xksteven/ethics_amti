# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--batch_size', '-s', type=int, default=100)  # NOTE: actually results in twice this number because two sentences per trait
parser.add_argument('--batch', '-b', type=int, default=0)
parser.add_argument('--nsamples', '-n', type=int, default=10)  # per batch
args = parser.parse_args()

df = pd.read_csv("data_to_curate/util.tsv", sep="\t", header=None)
begin, end = args.batch*args.batch_size, (args.batch+1)*args.batch_size
df = df[begin:end]
nbatches = df.shape[0] // args.nsamples

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

# will later have a list of traits 8 additional traits for each scenario, for for now let's just get the two default ones

list_of_dicts = []  # will save these dicts
for i in range(nbatches):
    for j in range(4):  # each pair
        d = {}
        for k in range(args.nsamples):  # TODO: batch
            idx = args.nsamples*i + k
            s1, s2 = df.iloc[idx, j], df.iloc[idx, j+1]

            # half the time swap the order
            if np.random.random() < 0.5:
                new_d = {"left{}".format(k): s1, "right{}".format(k): s2, "idx{}".format(k): str(idx), "swapped{}".format(k): "false", "v0_{}".format(k): "idx{:04d}_j{}_ex1".format(idx, j), "v1_{}".format(k): "idx{:04d}_j{}_ex2".format(idx, j+1), "v2_{}".format(k): "idx{:04d}_j{}_amb".format(idx, j)}
            else:
                new_d = {"left{}".format(k): s2, "right{}".format(k): s1, "idx{}".format(k): str(idx), "swapped{}".format(k): "true", "v0_{}".format(k): "idx{:04d}_j{}_ex2".format(idx, j+1), "v1_{}".format(k): "idx{:04d}_j{}_ex1".format(idx, j), "v2_{}".format(k): "idx{:04d}_j{}_amb".format(idx, j)}

            d.update(new_d)
        list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

