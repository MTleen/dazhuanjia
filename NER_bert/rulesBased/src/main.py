import os
import sys
import tqdm
sys.path.append('.')
import argparse
from data_process import *

def find_relation_by_dict():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=None, type=str, required=True,
                        help="The task data directory.")
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The path of result data.")
    parser.add_argument("--file_name", default=None, type=str, required=True,
                        help="The name of input data.")
    parser.add_argument("--dict_dir", default=None, type=str, required=True,
                        help="The dict of object.")
    args = parser.parse_args()

    # 加载正则
    object_dict = load_dict(os.path.join(args.dict_dir, 'dict.json'))

    # 读取数据和分词词典
    all_line, entities = read_from_json(os.path.join(args.data_dir, args.file_name + '.json'), lineform=False)
    all_schemas = []

    # 查找关系
    for line, current_dict in tqdm.tqdm(zip(all_line, entities)):
        schema = {'text': line['text'], 'spo_list': []}

        # 找到所有候选客体
        object_list = find_all_object(object_dict, line['text'], current_dict, mode=1, dict_first=False)
        # 排序
        if len(object_list) != 0:
            object_list = sorted(object_list, key=lambda x:(x[1],x[2]))

        # 为每个主体匹配客体
        for s in line['subject_list']:
            spo = {'subject': '', 'sub_position': 0, 'object': '', 'ob_position': 0}
            object = find_object(object_list, s['subject'], s['sub_position'], max_distance=10)
            if object != None:
                schema['spo_list'].append(spo)
                spo['subject'] = s['subject']
                spo['sub_position'] = s['sub_position']
                spo['object'] = object[0]
                spo['ob_position'] = object[1]
        all_schemas.append(schema)
    
    # 写文件
    with open(os.path.join(args.output_dir, args.file_name + '_IE_result.json'), 'w', encoding='utf-8') as w:
        w.write(json.dumps(all_schemas, ensure_ascii=False))


if __name__ == '__main__':
    find_relation_by_dict()
