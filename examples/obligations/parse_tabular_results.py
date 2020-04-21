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

#example = {"HITId": "39XCQ6V3KY4ANVXPEASRAXTSLFJ652", "AssignmentDurationInSeconds": 3600, "AutoApprovalDelayInSeconds": 259200, "Expiration": "2021-04-11T22:44:52-05:00", "CreationTime": "2020-04-11T22:44:52-05:00", "AssignmentId": "3F6KKYWMNB1GKDG4IZ1TZ4ZW9GNND8", "WorkerId": "A171OY96XOQ3IF", "AssignmentStatus": "Approved", "AutoApprovalTime": "2020-04-14T23:57:30-05:00", "AcceptTime": "2020-04-11T23:55:24-05:00", "SubmitTime": "2020-04-11T23:57:30-05:00", "ApprovalTime": "2020-04-12T10:57:55-05:00", "not_wrong": "he bumped the woman", "wrong": "he hit the woman"}

output_str = []
for entry in data:
    tmp = []
    tmp.append("0")
    tmp.append(entry["not_wrong"])
    tmp.append(entry["WorkerId"])
    tmp.append(entry["AssignmentId"])
    output_str.append(tmp)
    tmp = []
    tmp.append("1")
    tmp.append(entry["wrong"])
    tmp.append(entry["WorkerId"])
    tmp.append(entry["AssignmentId"])
    output_str.append(tmp)

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"

print(f"save_name = {save_name}")
with open(save_name, "w") as f:
    for entry in output_str:
        tmp = "\t".join(entry)
        tmp = tmp + "\n"
        f.write(tmp)

