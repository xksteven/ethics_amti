# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--batch_size', '-s', type=int, default=25)  # NOTE: actually results in twice this number because two sentences per trait
parser.add_argument('--batch', '-b', type=int, default=0)
parser.add_argument('--ntraits', '-n', type=int, default=8)
args = parser.parse_args()

df = pd.read_csv("data_to_curate/ve.tsv", sep="\t", header=None)
begin, end = args.batch*args.batch_size, (args.batch+1)*args.batch_size
df = df[begin:end]

savefile = "data.jsonl"

trait_df = pd.read_csv("parsed_traits.csv", header=None)

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

# will later have a list of traits 8 additional traits for each scenario, for for now let's just get the two default ones

list_of_dicts = []  # will save these dicts
for i in range(df.shape[0]):
    # two scenarios
    s1, s2 = df.iloc[i, 0], df.iloc[i, 1]
    t1, t2 = df.iloc[i, 2], df.iloc[i, 3]

    # two dicts.
    d1 = {"scenario": s1, "idx": str(i), "batch_size": str(args.batch_size), "batch": str(args.batch), "trait1": t1, "trait2": t2}
    d2 = {"scenario": s2, "idx": str(i), "batch_size": str(args.batch_size), "batch": str(args.batch), "trait1": t1, "trait2": t2}
    for j in range(8):
        # get random traits
        d1["trait{}".format(j+3)] = trait_df.sample().values[0, 1]
        d2["trait{}".format(j+3)] = trait_df.sample().values[0, 1]

    list_of_dicts.append(d1)
    list_of_dicts.append(d2)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

