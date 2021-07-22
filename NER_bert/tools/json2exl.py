import xlrd
# import xlwt
import json
import os
import sys
import xlsxwriter as xlwt
import tqdm
import re


def json2xls(output_dir, file_name, lines, flag=0):
    # print(lines)
    # workbook = xlwt.Workbook()

    RESULT_PATH = output_dir
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    RESULT_NAME = file_name

    cls2type = {
        'bod': '身体部分',
        'pro': '医疗程序',
        'dis': '疾病',
        'sym': '临床表现',
        'equ': '医疗设备',
        'dru': '药物',
        'ite': '医学检验项目',
        'dep': '科室',
        'mic': '微生物类',
        'sur': '手术'
    }

    pos2type = {'number': '数值', 'value': '描述', 'negative': '否定'}

    key2col = {
        'text': '原始病历',
        'type': '实体类型',
        'entity': '医疗实体',
        'std': '标准化',
        'object': '关系客体',
        'pos': '客体类型',
        'sub_seq': '关系所在子句'
    }

    if flag:
        RESULT_NAME += '_noempty.xls'
    else:
        RESULT_NAME += '_withempty.xls'
    max_num_persheet = 100
    sheet_count = len(lines) // max_num_persheet + 1

    workbook = xlwt.Workbook(os.path.join(RESULT_PATH, RESULT_NAME))
    worksheet_l = [
        workbook.add_worksheet(f'NER_{i+1}') for i in range(sheet_count)
    ]
    format_top = workbook.add_format({
        'border': 1,
        'bold': True,
        'text_wrap': True
    })
    format_other = workbook.add_format({'border': 1, 'valign': 'vcenter'})
    format_merge = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'text_wrap': True
    })

    for i in tqdm.tqdm(range(len(worksheet_l))):
        # for i, worksheet in tqdm.tqdm(enumerate(worksheet_l)):
        # print('current sheet:', i)
        worksheet = worksheet_l[i]
        count = 1
        for j, col in enumerate(key2col.values()):  #写表头
            #print(value)
            worksheet.write(0, j, col, format_top)
        for line in range(i * max_num_persheet, (i + 1) * max_num_persheet):
            if line < len(lines):
                json_data = lines[line]
            else:
                break

            entity_count = count
            entity_count_end = count
            # 遍历每个实体
            for idx, entity in enumerate(json_data['entities']):
                # 写关系抽取结果
                col_name = list(key2col.keys())[1:]
                init_col_idx = len(col_name[:-3]) + 1
                # 关系列表
                obj_list = entity.get('object_list', [])
                for obj_idx, spo in enumerate(obj_list):
                    for offset, key in enumerate(col_name[-3:]):
                        worksheet.write(
                            entity_count + obj_idx,
                                        init_col_idx + offset, 
                                        spo[key] if not spo[key] in pos2type else pos2type[spo[key]],
                                        format_other)
                entity_count_end = entity_count + max(len(obj_list) - 1, 0)

                for col_idx, key in enumerate(list(key2col.keys())[1:-3]):
                    if key == 'type':
                        content = cls2type[entity[key]]
                    elif key == 'std':
                        # if len(entity[key]) > 0:
                        std_val = [[item[0], '{:.4f}'.format(item[1])]
                                   for item in entity[key]]
                        content = json.dumps(std_val, ensure_ascii=False)
                    else:
                        content = entity[key]
                    if entity_count_end > entity_count:
                        worksheet.merge_range(entity_count, col_idx + 1,
                                              entity_count_end, col_idx + 1,
                                              content, format_merge)
                    else:
                        worksheet.write(entity_count, col_idx + 1, content,
                                        format_other)
                entity_count = entity_count_end + 1

            # 合并 原始病历 单元格
            if flag == 1 and len(json_data['entities']) <= 0:
                continue
            else:
                end = entity_count_end
                if count < end:
                    worksheet.merge_range(count, 0, end, 0, json_data['text'],
                                          format_merge)
                else:
                    worksheet.write(count, 0, json_data['text'], format_merge)
                # 每条记录之间添加空行
                # worksheet.write_merge(end + 1, end + 1, 0, 3, ' ')

            count = end + 1

    # workbook.save(os.path.join(RESULT_PATH, RESULT_NAME))
    workbook.close()


if __name__ == '__main__':
    file_dir = 'data/result_output/ie_out'
    output_dir = './data/result_output/excel_out'
    for file_name in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file_name)
        print('current file:', file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        out_name = re.search('.*_(shdx_.+jb)_.*', file_name).groups()[0]
        json2xls(output_dir, out_name, data)