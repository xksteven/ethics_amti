# simple task generator double check the max Assignments
import argparse
import numpy as np


parser = argparse.ArgumentParser(description='Create tasks to validate.')
parser.add_argument('hits', type=int, default=360, help='how many validate ordinary morality hits to submit')
parser.add_argument('-s', '--skip', type=int, default=0, help='from where in the dataset to submit.')
parser.add_argument('--num_samples', type=int, default=10, help='number of samples used per hit')
args = parser.parse_args()

#with open("data_to_curate/mturk_data_bad.csv", "r") as f:
with open("data_to_curate/all_remaining_to_clean.tsv", "r") as f:
    mturk_data = f.readlines()

tmp = []
for i in range(len(mturk_data)):
    tmp.append(mturk_data[i].strip().replace("\"","").split("\t"))
mturk_data = np.array(tmp)

skip_amount = (args.num_samples) * args.skip
mturk_data = mturk_data[skip_amount:]

upto = min(args.hits, len(mturk_data))

my_str = []
for index in range(0,(upto)):
    tmp_str = "{"
    for i in range(args.num_samples):
        sent_to_insert = mturk_data[index*args.num_samples+i][1]
        if i == (args.num_samples - 1):
            tmp_str += ("\"sent"+str(i)+"\" : \"" + str(sent_to_insert) + "\"")
        else:
            tmp_str += ("\"sent"+str(i)+"\" : \"" + str(sent_to_insert) + "\",")
    my_str.append(tmp_str+"}\n")

with open("data.jsonl", "w") as f:
    for i in range(len(my_str)):
        f.write(my_str[i])

#sandbox qual ID = 3N5C8MI2ZB0D7EPGZHGD8HJCAK82GM
