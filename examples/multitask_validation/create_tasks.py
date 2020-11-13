# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json
from sklearn.utils import shuffle

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--hits', type=int, default=500, help='how many hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=10, help='')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/test_shuffled.csv", header=None)
df = df[args.skip:args.skip + args.num_samples*args.hits]

savefile = "data.jsonl"

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

list_of_dicts = []  # will save these dicts
for i in range(df.shape[0] // args.num_samples):
    d = {}
    for j in range(args.num_samples):
        idx = df.index[i*args.num_samples+j]
        # question = df.iloc[i*args.num_samples + j, 1]
        # question += "<br>A. {}".format(df.iloc[i * args.num_samples + j, 2])
        # question += "<br>B. {}".format(df.iloc[i * args.num_samples + j, 3])
        # question += "<br>C. {}".format(df.iloc[i * args.num_samples + j, 4])
        # question += "<br>D. {}".format(df.iloc[i * args.num_samples + j, 5])
        # d["question{}".format(j)] = question
        d["button_{}A".format(j)] = "button_a_idx{}".format(idx)
        d["button_{}B".format(j)] = "button_b_idx{}".format(idx)
        d["button_{}C".format(j)] = "button_c_idx{}".format(idx)
        d["button_{}D".format(j)] = "button_d_idx{}".format(idx)
        d["question{}".format(j)] = df.iloc[i*args.num_samples + j, 1].replace("\n", "<br>")
        d["option_{}A".format(j)] = df.iloc[i*args.num_samples + j, 2].replace("\n", "<br>")
        d["option_{}B".format(j)] = df.iloc[i*args.num_samples + j, 3].replace("\n", "<br>")
        d["option_{}C".format(j)] = df.iloc[i*args.num_samples + j, 4].replace("\n", "<br>")
        d["option_{}D".format(j)] = df.iloc[i*args.num_samples + j, 5].replace("\n", "<br>")
    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        f.write("{}\n".format(mydict(d)))

