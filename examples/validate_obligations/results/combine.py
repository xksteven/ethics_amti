import os
import pandas as pd

ob = pd.read_csv("ob.tsv", sep="\t", header=None)
# print(ob)
# print(ob.iloc[0, 0])
# print(ob.iloc[0, 4])
# print(ob.iloc[0, 5])
# quit()

scenarios = []
reasonable_excuses = []
unreasonable_excuses = []
idxs = []

files = [f for f in os.listdir(".") if "batch" in f]
for file in files:
    df = pd.read_csv(file, sep="\t", header=None)
    for i in range(df.shape[0]):
        idx = df.iloc[i, 0]

        # first get the scenario
        idxs.append(idx)
        scenario = ob.iloc[idx, 0]
        scenarios.append(scenario)
        reasonable = []
        for j in range(3):
            reasonable.append(ob.iloc[idx, 1+j])
        reasonable_excuses.append(reasonable)
        unreasonable = [ob.iloc[idx, 4]]
        unreasonable += eval(df.iloc[i, 1])
        unreasonable_excuses.append(unreasonable)

        # print(idx)
        # print(scenario)
        # print(reasonable)
        # print(unreasonable)

results = {"idxs": idxs, "scenarios": scenarios, "reasonable_excuses": reasonable_excuses, "unreasonable_excuses": unreasonable_excuses}
results = pd.DataFrame(results)
results = results.sort_values("idxs")
results.to_csv("combined.tsv", sep="\t", header=None, index=None)
