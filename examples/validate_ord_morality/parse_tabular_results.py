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

#second index maps
#0 is not wrong
#1 is not wrong

key_to_index = {"wrong": 0, "not wrong": 1}
output = {}
for i, entry in enumerate(data):
    tmp = json.loads(entry["taskAnswers"])
    #print(tmp, type(tmp))
    for index, assignment in enumerate(tmp[0]):
        #print(assignment, tmp[0])
        wrong_id, ass_id = (assignment[1], assignment[2:])
        wrong_or_not = list(tmp[0][assignment].keys())[0]
        wrong_or_not_index = key_to_index[wrong_or_not]
        wrong_or_not_sel = int(tmp[0][assignment][wrong_or_not])
        tmp_ass = output.get(ass_id)
        #if i > 2:
        #    exit()
        #print("\n\n", tmp[0], assignment)
        #print(wrong_id, wrong_or_not, wrong_or_not_index, wrong_or_not_sel)
        if not tmp_ass:
            output[ass_id] = {wrong_id: [0,0]}
        if not output[ass_id].get(wrong_id):
            output[ass_id].update({wrong_id: [0,0]})
        output[ass_id][wrong_id][wrong_or_not_index] += wrong_or_not_sel

#TODO worker success rate

save_name = args.save_path + args.json.split("/")[-2] + ".tsv"

print(f"save_name = {save_name}")
with open(save_name, "w") as f:
    for index, entry in enumerate(output):
        for wr_or_not in output[entry]:
            tmp = ""
            tmp += entry + "\t"
            tmp += (wr_or_not + "\t" + 
                    str(output[entry][wr_or_not][0]) + "\t" +  str(output[entry][wr_or_not][1]))
            tmp = tmp + "\n"
            f.write(tmp)
            #print(tmp,  "\n\n", output[entry])
