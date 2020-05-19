# simple task generator double check the max Assignments
import argparse
import numpy as np
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('--batch_size', '-s', type=int, default=500, help='how many validate ordinary morality hits to submit')
parser.add_argument('--batch', '-b', type=int, default=0, help='from where in the dataset to submit.')
# parser.add_argument('--num_samples', type=int, default=4, help='')
args = parser.parse_args()

df = pd.read_csv("data_to_curate/ob.tsv", sep="\t", header=None)
begin, end = args.batch*args.batch_size, (args.batch+1)*args.batch_size
df = df[begin:end]

savefile = "data.jsonl"


class mydict(dict):
    def __str__(self):
        return json.dumps(self)

# will later have a list of traits 8 additional traits for each scenario, for for now let's just get the two default ones

list_of_dicts = []  # will save these dicts
for i in range(df.shape[0]):
    s = df.iloc[i, 0]
    id = df.iloc[i, -1]
    # d = {"scenario": s, "worker_id": id, "idx": i}
    d = mydict({"scenario": s, "idx": str(i), "batch_size": str(args.batch_size), "batch": str(args.batch)})
    list_of_dicts.append(d)

with open("data.jsonl", "w") as f:
    for d in list_of_dicts:
        # f.write("{}\n".format(d).replace("\'", "\""))
        f.write("{}\n".format(d))

# print(json.dumps(list_of_dicts)[1:-1])

# with open("data_to_curate/gt_data.csv", "r") as f:
#     gt_data = f.readlines()
#
# tmp = []
# for i in range(len(gt_data)):
#     tmp.append(gt_data[i].strip().replace("\"","").split("\t"))
# gt_data = np.array(tmp)
# gt_indices = np.load("data_to_curate/gt_indices.npy")
# gt_data = gt_data[gt_indices]
#
# skip_amount = args.skip
# gt_data = gt_data[skip_amount:]
#
# with open("data_to_curate/mturk_data.csv", "r") as f:
#     mturk_data = f.readlines()
#
# tmp = []
# for i in range(len(mturk_data)):
#     tmp.append(mturk_data[i].strip().replace("\"","").split("\t"))
# mturk_data = np.array(tmp)
# mturk_indices = np.load("data_to_curate/mturk_indices.npy")
# mturk_data = mturk_data[mturk_indices]
#
# skip_amount = (args.num_samples - 1) * args.skip
# mturk_data = mturk_data[skip_amount:]
#
# upto = min(args.hits, len(mturk_data))
#
# my_str = []
# for index in range(0,(upto)):
#     tmp_str = "{"
#     for i in range(args.num_samples):
#         if i < 2:
#             tmp = mturk_data[index*(args.num_samples-1) + i]
#             sent_to_insert = tmp[1]  # sentence
#             assign_id0 = str(0) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
#             assign_id1 = str(1) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
#         elif i == 2:
#             tmp = gt_data[index]
#             sent_to_insert = tmp[1]
#             assign_id0 = str(0) + str(tmp[0]) + str("ADan") + str(args.skip + index)
#             assign_id1 = str(1) + str(tmp[0]) + str("ADan") + str(args.skip + index)
#         else:
#             tmp = mturk_data[index*(args.num_samples-1) + i-1]
#             sent_to_insert = tmp[1]
#             assign_id0 = str(0) + str(tmp[0]) + str(tmp[3].strip())# original label, assignmentID
#             assign_id1 = str(1) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
#         #print(sent_to_insert, assign_id, type(assign_id))
#         #print(tmp_str)
#         if i == (args.num_samples - 1):
#             tmp_str += ("\"sample"+str(i)+"\" : \"" + str(sent_to_insert) + "\", " +
#                     "\"v" + str(2*i) + "\" : \"" + str(assign_id0) + "\", " +
#                     "\"v" + str(2*i+1) + "\" : \"" + str(assign_id1) + "\"")
#         else:
#             tmp_str += ("\"sample"+str(i)+"\" : \"" + str(sent_to_insert) + "\", " +
#                     "\"v" + str(2*i) + "\" : \"" + str(assign_id0) + "\", " +
#                     "\"v" + str(2*i+1) + "\" : \"" + str(assign_id1) + "\", ")
#     my_str.append(tmp_str+"}\n")
#
# with open("data.jsonl", "w") as f:
#     for i in range(len(my_str)):
#         f.write(my_str[i])

#sandbox qual ID = 3N5C8MI2ZB0D7EPGZHGD8HJCAK82GM
