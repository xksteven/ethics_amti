import argparse
import json

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

with open(args.json, "r") as f:
    tmp = f.readlines()
    data = [json.loads(line.strip()) for line in tmp]

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
