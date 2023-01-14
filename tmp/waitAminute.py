import os

l = os.listdir("../data/evaluation_tests")[1:]

found_names = []
diz = {"GEO": 0,
       "RND": 0,
       "QL": 0,
       "NQL": 0}

for name in l:
    if "simulation" in name:
        found_names.append(name)
        if "GEO" in name:
            diz["GEO"] += 1
        elif "RND" in name:
            diz["RND"] += 1
        elif ".QL" in name:
            diz["QL"] += 1
        elif "NQL" in name:
            diz["NQL"] += 1

print(len(found_names))
print(diz)
