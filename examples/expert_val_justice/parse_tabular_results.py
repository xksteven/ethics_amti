import argparse
import json

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

with open(args.json, "r") as f:
    tmp = f.readlines()
    #print(tmp, type(tmp))
    data = [json.loads(line.strip()) for line in tmp]

output_str = []
for entry in data:
    tmp = []
    tmp.append(entry["sentence0"])
    tmp.append(entry["sentence1"])
    tmp.append(entry["sentence2"])
    tmp.append(entry["sentence3"])
    tmp.append(entry["sentence4"])
    tmp.append(entry["sentence5"])
    tmp.append(entry["sentence6"])
    tmp.append(entry["sentence7"])
    tmp.append(entry["sentence8"])
    tmp.append(entry["sentence9"])
    tmp.append(entry["WorkerId"])
    tmp.append(entry["AssignmentId"])
    output_str.append(tmp)

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"
# save_name = args.save_path + args.json.split(".")[0] + ".tsv"

print(f"save_name = {save_name}")
with open(save_name, "w") as f:
    for entry in output_str:
        tmp = "\t".join(entry)
        tmp = tmp + "\n"
        f.write(tmp)

