# simple task generator double check the max Assignments
import argparse
import numpy as np


parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('hits', type=int, default=10, help='how many validate ordinary morality hits to submit')
parser.add_argument('which_batch', type=int, default=0, help='which batch to submit. Multiplies hits by this number to get.')
parser.add_argument('--num_samples', type=int, default=4, help='')
args = parser.parse_args()

with open("data_to_curate/gt_data.csv", "r") as f:
    gt_data = f.readlines()

tmp = []
for i in range(len(gt_data)):
    tmp.append(gt_data[i].strip().replace("\"","").split("\t"))
gt_data = np.array(tmp)
gt_indices = np.load("data_to_curate/gt_indices.npy")
gt_data = gt_data[gt_indices]

skip_amount = args.hits * args.which_batch
gt_data = gt_data[skip_amount:]

with open("data_to_curate/mturk_data.csv", "r") as f:
    mturk_data = f.readlines()

tmp = []
for i in range(len(mturk_data)):
    tmp.append(mturk_data[i].strip().replace("\"","").split("\t"))
mturk_data = np.array(tmp)
mturk_indices = np.load("data_to_curate/mturk_indices.npy")
mturk_data = mturk_data[mturk_indices]

skip_amount = (args.num_samples - 1) * args.hits * args.which_batch
mturk_data = mturk_data[skip_amount:]

upto = min(args.hits, len(mturk_data))

my_str = []
for index in range(0,(upto)):
    tmp_str = "{"
    for i in range(args.num_samples):
        if i < 2:
            tmp = mturk_data[index*(args.num_samples-1) + i]
            sent_to_insert = tmp[1]  # sentence
            assign_id0 = str(0) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
            assign_id1 = str(1) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
        elif i == 2:
            tmp = gt_data[index]
            sent_to_insert = tmp[1]
            assign_id0 = str(0) + str(tmp[0]) + str("ADan") + str(args.hits * args.which_batch + index)
            assign_id1 = str(1) + str(tmp[0]) + str("ADan") + str(args.hits * args.which_batch + index)
        else:
            tmp = mturk_data[index*(args.num_samples-1) + i-1]
            sent_to_insert = tmp[1]
            assign_id0 = str(0) + str(tmp[0]) + str(tmp[3].strip())# original label, assignmentID
            assign_id1 = str(1) + str(tmp[0]) + str(tmp[3].strip()) # original label, assignmentID
        #print(sent_to_insert, assign_id, type(assign_id))
        #print(tmp_str)
        if i == (args.num_samples - 1):
            tmp_str += ("\"sample"+str(i)+"\" : \"" + str(sent_to_insert) + "\", " + 
                    "\"v" + str(2*i) + "\" : \"" + str(assign_id0) + "\", " +
                    "\"v" + str(2*i+1) + "\" : \"" + str(assign_id1) + "\"")
        else:
            tmp_str += ("\"sample"+str(i)+"\" : \"" + str(sent_to_insert) + "\", " + 
                    "\"v" + str(2*i) + "\" : \"" + str(assign_id0) + "\", " + 
                    "\"v" + str(2*i+1) + "\" : \"" + str(assign_id1) + "\", ")
    my_str.append(tmp_str+"}\n")

with open("data.jsonl", "w") as f:
    for i in range(len(my_str)):
        f.write(my_str[i])

#sandbox qual ID = 3N5C8MI2ZB0D7EPGZHGD8HJCAK82GM
