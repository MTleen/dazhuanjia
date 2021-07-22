import re
import json
import os
import ijson
import tqdm
import argparse

reg_pattern = [
    (r'[\\n\\r\\]|\'| |\s|".*"|[\\u\\x][\da-f]+', ''), # 删除 \\n, ', 和 "" 之间的内容
    (r'(?<=[,.，。])[,.，。]+', ''), # 删除连续标点符号
    (r'．', '.'),
    (r'(?<=[\u4e00-\u9fa5])[,.?:](?=[\u4e00-\u9fa5])', '，'), # 修改两个中文字符之间的英文标点为中文标点
    (r'[,，;；:：.?？]$', '。'),
    (r'^[,.，。、？?:：]', '')
]

def preprocess(text, reg_pattern):
    for p in reg_pattern:
        text = re.sub(p[0], p[1], text)
    return text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', default=['shdx_guke_fangdajb.json', 'shdx_guke_ptjb.json', 'shdx_xiaohua_fangdajb.json', 'shdx_xiaohua_ptjb.json'], required=False, nargs='+')
    parser.add_argument('--data_dir', default='testData', type=str, required=False)
    parser.add_argument('--max_len', default=20, type=int, required=False)
    args = parser.parse_args()

    file_name = args.file_name
    data_dir = args.data_dir
    max_len = args.max_len

    for i, file in enumerate(file_name):
        input_path = os.path.join(data_dir, file)
        if max_len > 0:
            output_path = os.path.join(data_dir, f'{os.path.splitext(file)[0]}_clean_{max_len}.json')
        else:
            output_path = os.path.join(data_dir, f'{os.path.splitext(file)[0]}_clean.json')
        print(f'********** processing file {i+1}/{len(file_name)}: {input_path} *************')
        f = open(input_path, 'r', encoding='utf-8')
        lines = ijson.items(f, 'item')
        output_f = open(output_path, 'w', encoding='utf-8')
        count = 0
        for line in tqdm.tqdm(lines):
            if max_len > 0:
                if count < max_len:
                    output_f.writelines(json.dumps({'text': preprocess(line['text'], reg_pattern)}, ensure_ascii=False) + '\n')
                    count += 1
                else:
                    break
            else:
                output_f.writelines(json.dumps({'text': preprocess(line['text'], reg_pattern)}, ensure_ascii=False) + '\n')
        f.close()
        output_f.close()