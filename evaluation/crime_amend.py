import json
from crime_extraction import get_crime

res = []
with open('/home/ubuntu/JuDGE_edit/data/all.json','r') as f:
    data = json.load(f)
    for item in data:
        item["Crime Type"] = get_crime(item["Full Document"])
        # if set(item["crime_judge"]) != set(item["Crime Type"]):
        #     print(item["crime_judge"],item["Crime Type"])
        res.append(item)

with open('/home/ubuntu/JuDGE_edit/data/all_amend.json','w') as f:
    json.dump(res,f,ensure_ascii=False,indent=4)
