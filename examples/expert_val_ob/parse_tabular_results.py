import argparse
import json
import pandas as pd

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
all_sentences = []
for entry in data:
    # print(entry)

    idxs = []
    for key in entry:
        if "bad" in key:
            idx = int(key.split("bad_")[1].split(".")[0])
            idxs.append(idx)
    # print(idxs)

    labels = []
    for idx in idxs:
        for beginning, ending in zip(["good", "bad", "low_quality"], ["reasonable", "not reasonable", "low quality"]):
            key = "{}_{}.{}".format(beginning, idx, ending)
            is_true = eval(entry[key].replace("true", "True").replace("false", "False"))

            if "good" == beginning and is_true:
                label = "good"
                labels.append(label)
            elif "bad" == beginning and is_true:
                label = "bad"
                labels.append(label)
            elif "low_quality" == beginning and is_true:
                label = "low_quality"
                labels.append(label)

    try:
        sentences = [entry["sentence{}".format(k)] for k in range(10)]
        orig_sentences = [entry["orig_sentence{}".format(k)] for k in range(10)]
        changed_sentence_idxs = []
        for i in range(10):
            if sentences[i] != orig_sentences[i]:
                changed_sentence_idxs.append(i)
        print("changed sentence idxs", changed_sentence_idxs)
    except:
        print("problem", entry)

    all_idxs += idxs
    all_labels += labels
    all_sentences += sentences

df = pd.DataFrame({"idxs": all_idxs, "labels": all_labels, "sentences": all_sentences})
print(df)

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"
df.to_csv(save_name, sep="\t", header=None, index=None)


