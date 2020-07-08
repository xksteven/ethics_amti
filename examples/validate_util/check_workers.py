import argparse
import json
import numpy as np
import pickle
import pandas as pd

parser = argparse.ArgumentParser(description="Parse the tabular data from Mturk and save to csv.")
parser.add_argument("json", type=str, help="path to json file")
parser.add_argument("--save_path", type=str, default="./")
args = parser.parse_args()

with open(args.json, "r") as f:
    tmp = f.readlines()
    data = [json.loads(line.strip()) for line in tmp]

results = {}
for d in data:
    answers = eval(d["taskAnswers"].replace("false", "False").replace("true", "True"))[0]
    worker = d["WorkerID"]
    print(worker, answers)
    quit()
