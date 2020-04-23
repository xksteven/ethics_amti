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

# example {"HITId": "3K3IX1W4S6RF37RBO2IHO80V840PAZ", "AssignmentDurationInSeconds": 1800,
#"AutoApprovalDelayInSeconds": 259200, "Expiration": "2020-04-20T10:19:56-05:00",
#"CreationTime": "2020-04-18T10:19:56-05:00", "AssignmentId": "35BLDD71I6XWVJU9C8CH0DCCK2FZVJ",
#"WorkerId": "A2EPDDX5049SYF", "AssignmentStatus": "Approved",
#"AutoApprovalTime": "2020-04-21T10:23:30-05:00", "AcceptTime": "2020-04-18T10:22:55-05:00", 
#"SubmitTime": "2020-04-18T10:23:30-05:00", "ApprovalTime": 1234,
#"taskAnswers": "[{\"003JV9LGBJWTE1EIQ7L42EKE2YCLHOGD\":{\"wrong\":false},\"0131EUONYN2V3KWFG2AZ10KF58ZJVOVU\":{\"wrong\":true},\"013IOEN3P9S7JELXU03PVHWRC1PW7164\":{\"wrong\":true},\"01ADan83\":{\"wrong\":true},\"103JV9LGBJWTE1EIQ7L42EKE2YCLHOGD\":{\"not wrong\":true},\"1131EUONYN2V3KWFG2AZ10KF58ZJVOVU\":{\"not wrong\":false},\"113IOEN3P9S7JELXU03PVHWRC1PW7164\":{\"not wrong\":false},\"11ADan83\":{\"not wrong\":false}}]"}

output_str = []
for entry in data:
    tmp = []
    tmp.append("0")
    tmp.append(entry["not_wrong"])
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

