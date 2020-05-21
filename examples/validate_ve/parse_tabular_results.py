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
            idx = int(key.split("_")[0][3:])  # same for each key
            j = int(key.split("_")[1])  # diff for each key, and increases in increments
            d = int(key[-1])  # same for each key

            # just check ans1 (trait good)
            if "ans1" in key:
                good = answers[key]["good"]
                res.append(good)

        # print(len(res))
        if (idx, d) in results:
            results[(idx, d)].append(res)
        else:
            results[(idx, d)] = [res]

np_results = {}
for idx in results.keys():
    list_of_lists = results[idx]
    array = np.array(list_of_lists)
    np_results[idx] = array

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"

df = pd.DataFrame({"results": np_results})
df.to_csv(save_name, sep="\t", header=None)

# print(np_results)
# print(len(np_results))

