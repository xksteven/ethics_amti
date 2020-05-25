import numpy as np
import pandas as pd

df = pd.read_csv("data_to_curate/ve.tsv", sep="\t", header=None)

ks = [2, 3, 4]

trait_lists = []
scenarios = []

for k in ks:
    batch = pd.read_csv("batch{}.tsv".format(k), sep="\t", header=None)
    data_file = open("data{}.jsonl".format(k), "r")
    # print(batch[:10])
    # if k == 4:
    #     for j in range(1, batch.shape[0]-1):
    #         idx_prev = batch.iloc[j-1, 0]
    #         idx = batch.iloc[j, 0]
    #         idx_after = batch.iloc[j+1, 0]
    #         if idx_prev != idx and idx_after != idx:
    #             print(idx)


    for i, line in enumerate(data_file):
        # print(batch.shape)
        # print(k, i)
        if len(line) < 3:
            break
        d = eval(line.strip())
        traits = [d["trait{}".format(l+1)] for l in range(10)]
        scenario = d["scenario"]
        # print(scenario, traits)
        # idx = i // 2
        # d = (i % 2) + 1

        labels = eval(batch.iloc[i].values[2].replace("e ", "e, ").replace("[ ", "[").replace("  ", " ").replace("]\n", "],\n"))
        avg_labels = np.array(labels).mean(0)

        # only keep a scenario if the first two traits are 1/0 or 0/1 respectively
        # if so, then also keep track of all of the
        if (avg_labels[0] < 0.01 and avg_labels[1] > 0.99) or (avg_labels[1] < 0.01 and avg_labels[0] > 0.99):
            # make sure the correct trait comes first

            if (avg_labels[0] < 0.01 and avg_labels[1] > 0.99):
                agreed_upon_traits = [traits[1], traits[0]]
            else:
                agreed_upon_traits = [traits[0], traits[1]]

            for j in range(len(traits)-2):
                j2 = j + 2
                if avg_labels[j2] < 0.01:
                    agreed_upon_traits.append(traits[j2])

            if len(agreed_upon_traits) > 5:
                scenarios.append(scenario)
                trait_lists.append(agreed_upon_traits)

    data_file.close()

df = pd.DataFrame({"scenarios": scenarios, "traits": trait_lists})
print(df)
df.to_csv("validated_ve.tsv", sep="\t", header=None)
