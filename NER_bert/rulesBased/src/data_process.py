import json
import re
from ltp import LTP

# 从json中读取待抽取关系的数据
def read_from_json(file_path, lineform=True):
    with open(file_path, 'r', encoding="utf-8") as f:
        # print(file_path)
        json_data = []
        entities_dict = []
        if lineform:
            lines = f.readlines()
        else:
            lines = json.load(f)

        for line in lines:
            if lineform:
                line = json.loads(line)
            else:
                pass      
            one_data = {'text': '', 'subject_list': []}
            one_data['text'] = line['text'].replace(' ','').replace('+', '＋').replace('\\xa', '')
            current_dict = [i['entity'] for i in line['entities']]
            for entity in line['entities']:
                if entity['type'] in ['ite', 'sym']:
                    one_data['subject_list'].append({'subject': entity['entity'], 'sub_position': entity['start_idx']})
            if len(one_data['subject_list']) > 0:
                json_data.append(one_data)
            entities_dict.append(current_dict)
        return json_data, entities_dict

# 加载正则字典
def load_dict(dict_path):
    with open(dict_path ,'r', encoding='utf-8') as f:
        line = json.load(f)
        object_dict = line['dict']
        return object_dict

# 查找所有数值客体
def find_all_object(object_dict, text, entity_dict, mode=1, dict_first=False):

    # 根据字典找数值
    object_list_dict = []
    if mode == 0 or mode == 1:
        for rstr in object_dict:
            candidate_object = re.compile(rstr).findall(text)
            for cob in candidate_object:
                for i in re.finditer(cob, text):
                        elm = (cob, i.start(), 0 - len(cob))
                        object_list_dict.append(elm)
        object_list_dict = list(set(object_list_dict))

    # 根据词法分析找字典
    object_list_pos = []
    if mode == 0 or mode == 2:
        ltp = LTP()
        ltp.add_words(words=entity_dict)
        seg, hidden = ltp.seg([text])
        pos = ltp.pos(hidden)
        for sg, ps in zip(seg, pos):
            now_index = 0
            for s, p in zip(sg, ps):
                if p == 'm':
                    flag = 0
                    if dict_first and mode == 0:
                        for i in object_list_dict:
                            if i in s:
                                flag = 1
                                break
                    if flag == 0:
                        elm = (s, now_index, 0 - len(s))
                        object_list_pos.append(elm)
                now_index += len(s)
    
    object_list = list(set(object_list_dict + object_list_pos))
    return object_list

# 确定主体对应的客体
def find_object(object_list, subject, subject_index, max_distance=10):
    object = None
    for o in object_list:
        if o[1] > subject_index and o[1] - (subject_index + len(subject)) <= max_distance:
            object = o
            break

    return object

