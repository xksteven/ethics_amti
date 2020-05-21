import argparse
import json
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

begin_idx = 0
end_idx = 199

results = {}
with open(args.json, "r") as f:
    for line in f:
        if len(line) < 3:
            break
        answers = eval(line[:-1])["taskAnswers"]
        answers = eval(answers.replace("true", "True").replace("false", "False"))[0]
        # print(answers)

        res = []
        for key in answers.keys():
            print(key)
            good = key[:4] == "good"
            if good:
                idx = int(key.split("_")[1][3:])
                is_good = answers[key]["not wrong"]

                if idx in results:
                    results[idx].append(1-is_good)
                else:
                    results[idx] = [1-is_good]

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"

df = pd.DataFrame({"results": results})
df.to_csv(save_name, sep="\t", header=None)

# print(np_results)
# print(len(np_results))

