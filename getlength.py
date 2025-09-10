import json
with open('theassetcontainment.json') as assetjson:
    theasset=json.load(assetjson)

count=0
for school in theasset:
    for degree in list(school)[1:]:
        count+=1
print(count)