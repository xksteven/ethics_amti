import numpy as np
import pandas as pd

v = 2

df = pd.read_csv("saved_data{}.tsv".format(v), sep="\t", header=None)
print(df.shape)

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

# n = df.shape[0] // 2
# require_good_pair = True

good_sentences = []
bad_sentences = []

# TODO: make sure things work even when not exactly two...
# Use edit distance.

# gather a list of lists
# loop through. keep track of previous sentence. check if current sentence has small edit distance.
# if so, add it to the most recent list. Otherwise, append the most recent list.
sets = []
set = []
prev = ""
for i in range(df.shape[0]):
    s = df.iloc[i, 0]
    if levenshteinDistance(s, prev) < 8:
        set.append(i)
        if i == df.shape[0] - 1:
            sets.append(set)
    else:
        sets.append(set)
        set = [i]

    prev = s

sets = sets[1:]  # remove empty set
size = 0
for set in sets:
    size += len(set) / len(sets)

keep_sentences = []
dont_keep_sentences = []
for set in sets:
    if len(set) < 2:
        dont_keep_sentences.append(df.iloc[i, 0])
        continue
    for j in range(10):
        sentences = []
        to_compare_sentences = []
        for i in set:
            sentences.append(df.iloc[i, j])
            to_compare_sentences.append(df.iloc[i, j].lower().replace(" ", "").replace(".", ""))

        # loop through pairs of sentences; see if at least two agree.
        keep = ""
        for k1 in range(1, len(set)):
            for k2 in range(k1):
                t1, t2 = to_compare_sentences[k1], to_compare_sentences[k2]
                if t1 == t2:
                    keep = sentences[k1]
        if keep:
            keep_sentences.append(keep)
        else:
            dont_keep_sentences.append(sentences[0])

print(len(dont_keep_sentences))
print(len(keep_sentences))
df_cleaned = pd.DataFrame({"sentences": keep_sentences})
df_cleaned.to_csv("cleaned_results{}.tsv".format(v), sep="\t", header=None)

# df_cleaned_good = pd.DataFrame({"good": good_sentences})
# df_cleaned_wrong = pd.DataFrame({"wrong": bad_sentences})
# df_cleaned_good.to_csv("cleaned_good_results4.tsv", sep="\t", header=None)
# df_cleaned_wrong.to_csv("cleaned_wrong_results4.tsv", sep="\t", header=None)

# now for each set, see if there is a pair that agrees. if so, write to file along with the index.

# for i in range(n):
#     for j in range(5):
#         # good/not wrong sentence
#         s1, s2 = df.iloc[2*i, 2*j], df.iloc[2*i+1, 2*j]
#         s1_l, s2_l = s1.lower().replace(" ", "").replace(".", ""), s2.lower().replace(" ", "").replace(".", "")
#
#         # bad/wrong sentence
#         t1, t2 = df.iloc[2*i, 2*j+1], df.iloc[2*i+1, 2*j+1]
#         t1_l, t2_l = t1.lower().replace(" ", "").replace(".", ""), t2.lower().replace(" ", "").replace(".", "")
#
#
#         if require_good_pair:
#             if s1_l == s2_l and t1_l == t2_l:
#                 # save to file
#                 good_sentences.append(s1)
#                 bad_sentences.append(t1)
#             else:
#                 if s1_l != s2_l:
#                     print(s1, s2)
#                 else:
#                     print(t1, t2)
#         else:
#             if s1_l == s2_l:
#                 # save to file
#                 good_sentences.append(s1)
#             if t1_l == t2_l:
#                 bad_sentences.append(t1)
#
#
# if require_good_pair:
#     df_cleaned = pd.DataFrame({"not_wrong": good_sentences, "wrong": bad_sentences})
#     df_cleaned.to_csv("cleaned_results4.tsv", sep="\t", header=None)
# else:
#     df_cleaned_good = pd.DataFrame({"good": good_sentences})
#     df_cleaned_wrong = pd.DataFrame({"wrong": bad_sentences})
#     df_cleaned_good.to_csv("cleaned_good_results4.tsv", sep="\t", header=None)
#     df_cleaned_wrong.to_csv("cleaned_wrong_results4.tsv", sep="\t", header=None)
