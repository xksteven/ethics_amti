# simple task generator double check the max Assignments
my_str = []
for i in range(1,1+30): 
    my_str.append("{\"a\": \""+str(i)+"\"}\n")
with open("data.jsonl", "w") as f:
    for i in range(len(my_str)):
        f.write(my_str[i])

