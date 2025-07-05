import json
from crime_extraction import get_crime
from judge_extraction import calc_time_sum, calc_amt_sum
from law_extraction import get_penalcode_index_from_text



with open("/home/ubuntu/JuDGE_edit/lecardv2-doc/lecardv2-doc_sample.json",'r') as f1, open("/home/ubuntu/JuDGE_edit/lecardv2-doc/lecardv2_sample_cail.json",'w') as f2:
    data = json.load(f1)
    for item in data:
        fd = item["Full Document"]
        time = calc_time_sum(fd)
        amt = calc_amt_sum(fd)
        
        dic = {}
        dic['fact'] = item["Fact"]
        dic['CaseId'] = item["CaseId"]
        meta = {}
        meta['punish_of_money'] = amt
        meta['accusation'] = [c[:-1] for c in item["Crime Type"]]
        meta['relevant_articles'] = [str(code) for code in item["Law Articles"]]
        meta['term_of_imprisonment'] = {"death_penalty": False, "imprisonment": 0, "life_imprisonment": False}
        if time >10000:
            meta['term_of_imprisonment']['death_penalty'] = True
        elif time == 240:
            meta['term_of_imprisonment']['life_imprisonment'] = True
        meta['term_of_imprisonment']['imprisonment'] = time
        dic['meta'] = meta
        f2.write(json.dumps(dic,ensure_ascii=False)+'\n')

