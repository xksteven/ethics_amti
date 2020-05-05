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

# {"HITId": "3Z33IC0JC0ME38E2I8DGY5ETODMV9K", "AssignmentDurationInSeconds": 1200,
#"AutoApprovalDelayInSeconds": 259200, "Expiration": "2020-04-22T17:51:45-05:00",
#"CreationTime": "2020-04-22T11:21:28-05:00", "AssignmentId": "3Z4AIRP3C6DR4CEW4C47W4PLOMXX1V",
#"WorkerId": "A6ORRFI3XOACA", "AssignmentStatus": "Submitted",
#"AutoApprovalTime": "2020-04-25T17:18:00-05:00", "AcceptTime": "2020-04-22T17:08:26-05:00",
# "SubmitTime": "2020-04-22T17:18:00-05:00", "ApprovalTime": 1234,
#"obligation": "Aren't you supposed to pray before you eat.",
#"response1": "But I pray once a day.", "response2": "But I am a nonbeliever.",
#"response3": "But I prayed last meal.", "response4": "But I snack without praying.",
#"response5": "But I am too hungry to wait.", "response6": "But I do not want to."}

output_str = []
for entry in data:
    tmp = []
    # tmp.append(entry["sentence1"])
    for i in range(1,6):
        if 'response' + str(i) in entry.keys():
            tmp.append(entry["sentence1"] + " " + entry["response"+str(i)])
        else:
            tmp.append(entry["sentence1"])
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

