import os
import json




LONG = {}
MEDIUM = {}
SHORT = {}

with open("words.txt", 'r') as f:
    for line in f.readlines():
        if len(line) <= 5:
            if line[0] not in SHORT:
                SHORT[line[0]] = [line[:-1]]
            else:
                SHORT[line[0]].append(line[:-1])
        elif len(line) > 5 and len(line) <= 9:
            if line[0] not in MEDIUM:
                MEDIUM[line[0]] = [line[:-1]]
            else:
                MEDIUM[line[0]].append(line[:-1])
        else:
            if line[0] not in LONG:
                LONG[line[0]] = [line[:-1]]
            else:
                LONG[line[0]].append(line[:-1])
# for key, value in SHORT.items():
#     for word in value:
#         print(key + " : " + word, end = ", ")
#     print()

with open('long.json', 'w') as fp:
    json.dump(LONG, fp)

with open('short.json', 'w') as fp:
    json.dump(SHORT, fp)

with open('medium.json', 'w') as fp:
    json.dump(MEDIUM, fp)