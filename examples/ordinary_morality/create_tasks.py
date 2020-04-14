# simple task generator double check the max Assignments
import argparse

my_str = []
for i in range(1,(1+500)//9): 
    my_str.append("{\"a\": \""+str(i)+"\"}\n")
with open("data.jsonl", "w") as f:
    for i in range(len(my_str)):
        f.write(my_str[i])

#sandbox qual ID = 3N5C8MI2ZB0D7EPGZHGD8HJCAK82GM
