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

# example {"HITId": "3JMNNNO3B14GIDT8N93XAKPTPFIW25", "AssignmentDurationInSeconds": 1200,
#"AutoApprovalDelayInSeconds": 259200, "Expiration": "2020-04-21T16:57:22-05:00",
#"CreationTime": "2020-04-21T11:57:06-05:00", "AssignmentId": "34X6J5FLPTYEQWTO8NFL6WPEKTSQJY",
#"WorkerId": "A3SCRQ4WF9NYEE", "AssignmentStatus": "Submitted",
#"AutoApprovalTime": "2020-04-24T15:10:48-05:00", "AcceptTime": "2020-04-21T15:06:02-05:00",
#"SubmitTime": "2020-04-21T15:10:48-05:00", "ApprovalTime": 1234,
#"scenario1": "When his mother came home from the store, Adam told her that he had broken the thermostat.",
#"scenario2": "When his mother came home from the store, Adam told her that the thermostat stopped working.",
#"trait1": "truthfulness", "trait2": "deceitfulness", "untrait1": "vanity", "untrait2": "bravery"}

output_str = []
for entry in data:
    tmp = []
    tmp.append(entry["scenario1"])
    tmp.append(entry["scenario2"])
    tmp.append(entry["trait1"])
    tmp.append(entry["trait2"])
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

