import argparse
import json
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

results = {}
with open(args.json, "r") as f:
    for line in f:
        if len(line) < 3:
            break
        elif line[-1] != "\n":  # for final line
            line += "\n"

        dict = eval(line[:-1])
        excuses = []
        for key in dict:
            if "idx" in key:
                excuse = dict[key]
                idx = int(key.split("_")[0][3:])
                d = int(key[-1])
                print(excuse)
                excuses.append(excuse)
        results[idx] = excuses

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"
print(results)

df = pd.DataFrame({"results": results})
df.to_csv(save_name, sep="\t", header=None)


