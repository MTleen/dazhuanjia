import xlrd
import xlwt
import json
import os
import sys
def main():
    workbook = xlwt.Workbook()
    

    RESULT_PATH = './data/result_output'
    RESULT_NAME = 'shdx_guke_ptjb'

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

    with open('./data/result_output/shdx_guke_ptjb.json', 'r', encoding='utf-8') as f:
        flag = 0
        lines = json.load(f)
        if flag:
            RESULT_NAME += '_test_noempty.xls'
        else:
            RESULT_NAME += '_test_withempty.xls'
        max_num_persheet = 100
        sheet_count = len(lines) // max_num_persheet + 1
        worksheet_l = [workbook.add_sheet(f'NER_{i+1}') for i in range(sheet_count)]
        # worksheet = workbook.add_sheet('test')
        for i, worksheet in enumerate(worksheet_l):
            print('current sheet:', i)
            count = 0
            for line in range(i * max_num_persheet, (i+1) * max_num_persheet):
                if line < len(lines):
                    json_data = lines[line]
                else:
                    break
                if flag == 1 and len(json_data['entities']) <= 0:
                    pass
                else:
                    end = count + len(json_data['entities']) - 1
                    if end < count:
                        end = count
                    worksheet.write_merge(count, end, 0, 0, json_data['text'])
                    worksheet.write_merge(end + 1, end + 1, 0, 3, ' ')

                for spo in json_data['entities']:
                    worksheet.write(count + json_data['entities'].index(spo), 1, cls2type[spo['type']])
                    worksheet.write(count + json_data['entities'].index(spo), 2, spo['entity'])

                count = end + 2

        workbook.save(os.path.join(RESULT_PATH, RESULT_NAME))

if __name__ == '__main__':
    main()