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

        answers = eval(line[:-1])["taskAnswers"]
        answers = eval(answers.replace("true", "True").replace("false", "False"))[0]

        res = []
        for key in answers.keys():
            reasonable = key[0] == "r"
            if reasonable:
                idx = int(key.split("_")[1][3:])
                k = int(key.split("_")[2][1])
                is_reasonable = answers[key]["reasonable"]

                if (idx, k) in results:
                    results[(idx, k)].append(is_reasonable)
                else:
                    results[(idx, k)] = [is_reasonable]

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"

df = pd.DataFrame({"results": results})
df.to_csv(save_name, sep="\t", header=None)


