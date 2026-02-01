from collections import Counter

random_string = "hrtbjgfvhbtjgnjkh"

repeated_1_strs = {}
myDict = dict(Counter(random_string))
for elem in myDict:
    repeated_1_strs[elem] = myDict[elem]