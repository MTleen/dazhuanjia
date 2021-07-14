import os
import sys
sys.path.append('.')
import json
import matplotlib.pyplot as plt

# with open('./CBLUEDatasets/CMeIE/CMeIE_train.json', 'r', encoding='utf-8') as f, open('./CBLUEDatasets/CMeIE/53_schemas.json', 'r', encoding='utf-8') as t:
#     schemas = t.readlines()
#     schema_list = []
#     for s in schemas:
#         schema_list.append(json.loads(s))
#     schema_num_list = [0] * len(schema_list)


    
#     lines = f.readlines()
#     for line in lines:
#        j_data = json.loads(line)
#        j_data_list = j_data["spo_list"]
#        for i in j_data_list:
#             class_ = {"subject_type": [], "predicate": [], "object_type": []}
#             class_["predicate"] = i["predicate"]
#             class_["subject_type"] = i["subject_type"]
#             class_["object_type"] = i["object_type"]["@value"]
#             if class_ in schema_list:
#                 schema_num_list[schema_list.index(class_)] += 1

#     result = []
#     for i in range(len(schema_list)):
#         a = {"subject_type": [], "predicate": [], "object_type": [], "num": 0}
#         a["predicate"] = schema_list[i]["predicate"]
#         a["subject_type"] = schema_list[i]["subject_type"]
#         a["object_type"] = schema_list[i]["object_type"]
#         a["num"] = schema_num_list[i]
#         result.append(a)
    
#     schema_num_list, schema_list = zip(*sorted(zip(schema_num_list, schema_list), key=lambda x:x[0], reverse=True))


#     labels = [str(k) for k in schema_list]
#     plt.bar(range(len(schema_num_list)), schema_num_list, tick_label=labels)
#     plt.savefig('result.png')


### 数据处理
with open('./CBLUEDatasets/CMeIE/53_schemas.json', 'r', encoding='utf-8') as sc, open('./CBLUEDatasets/CMeIE/CMeIE_dev_copy.json', 'r', encoding='utf-8') as rd, open('./CBLUEDatasets/CMeIE/CMeIE_dev.json', 'w', encoding='utf-8') as wt:
    schemas = sc.readlines()
    schema_list = []
    for s in schemas:
        schema_list.append(json.loads(s))

    lines = rd.readlines()
    for line in lines:
        line = json.loads(line)
        spo_list = line['spo_list']
        s_list = []
        for spo in spo_list:
            class_ = {"subject_type": '', "predicate": '', "object_type": ''}
            class_["predicate"] = spo["predicate"]
            class_["subject_type"] = spo["subject_type"]
            class_["object_type"] = spo["object_type"]["@value"]
            if class_ in schema_list:
                s_list.append(spo)

        if len(s_list) > 0:
            line['spo_list'] = s_list
            wt.write(json.dumps(line, ensure_ascii=False) + '\n')