# simple task generator double check the max Assignments
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('hits', type=int, help='how many utiliarianism hits to submit')

args = parser.parse_args()

my_str = []
# 9 is hard coded but it stands for the MAX_ASSIGNMENTS variable make sure it's less than 10
# otherwise we take an additional 20% loss in fees
for i in range(1,(1+args.hits)//1): 
    my_str.append("{\"a\": \""+str(i)+"\"}\n")
with open("data.jsonl", "w") as f:
    for i in range(len(my_str)):
        f.write(my_str[i])

#sandbox qual ID = 3N5C8MI2ZB0D7EPGZHGD8HJCAK82GM
