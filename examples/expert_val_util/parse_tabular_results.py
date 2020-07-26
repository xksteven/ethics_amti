import argparse
import json
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

with open(args.json, "r") as f:
    tmp = f.readlines()
    #print(tmp, type(tmp))
    data = [json.loads(line.strip()) for line in tmp]

output_str = []
all_idxs = []
all_labels = []
all_sentences0 = []
all_sentences1 = []
is_swapped = {}
for entry in data:
    idxs = []
    for key in entry:
        if "second" in key:
            idx = int(key.split("second_")[1].split(".")[0].split("_")[0])
            idxs.append(idx)

    labels = []
    for idx in idxs:
        for beginning, ending in zip(["first", "second", "low_quality"], ["first_better", "second_better", "low quality"]):
            for swap in ["is_swapped", "not_swapped"]:
                key = "{}_{}_{}.{}".format(beginning, idx, swap, ending)
                if key not in entry:
                    continue
                # key = "{}_{}.{}".format(beginning, idx, ending)
                is_true = eval(entry[key].replace("true", "True").replace("false", "False"))

                if idx not in is_swapped:
                    is_swapped[idx] = swap == "is_swapped"

                if "first" == beginning and is_true:
                    label = "first"
                    labels.append(label)
                elif "second" == beginning and is_true:
                    label = "second"
                    labels.append(label)
                elif "low_quality" == beginning and is_true:
                    label = "low_quality"
                    labels.append(label)

    try:
        sentences0 = [entry["sentence{}0".format(k)] for k in range(4)]
        sentences1 = [entry["sentence{}1".format(k)] for k in range(4)]
        orig_sentences0 = [entry["orig_sentence{}0".format(k)] for k in range(4)]
        orig_sentences1 = [entry["orig_sentence{}1".format(k)] for k in range(4)]
        changed_sentence_idxs = []
        for i in range(4):
            if sentences0[i] != orig_sentences0[i] or sentences1[i] != orig_sentences1[i]:
                changed_sentence_idxs.append(i)
        if len(changed_sentence_idxs) > 0:
            print("fraction changed sentence idxs", np.mean(changed_sentence_idxs))
    except:
        print("problem", entry)

    all_idxs += idxs
    all_labels += labels
    all_sentences0 += sentences0
    all_sentences1 += sentences1

is_swapped = [is_swapped[idx] for idx in all_idxs]
is_correct = []
swapped_sentences0 = []
swapped_sentences1 = []
for i in range(len(labels)):
    correct = (labels[i] == "first" and is_swapped[i] == False) or (labels[i] == "second" and is_swapped[i] == True)
    is_correct.append(correct)
    if is_swapped[i]:
        swapped_sentences0.append(sentences1[i])
        swapped_sentences1.append(sentences0[i])
    else:
        swapped_sentences0.append(sentences0[i])
        swapped_sentences1.append(sentences1[i])

# df = pd.DataFrame({"idxs": all_idxs, "labels": all_labels, "is_swapped": is_swapped, "sentences0": all_sentences0, "sentences1": all_sentences1})
df = pd.DataFrame({"idxs": all_idxs, "is_correct": is_correct, "sentences0": swapped_sentences0, "sentences1": swapped_sentences1})
print(df)

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"
df.to_csv(save_name, sep="\t", header=None, index=None)


