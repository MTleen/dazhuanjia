from typing import Mapping
import xlrd
import xlwt
import json
import os
import sys
import re
import pandas as pd


def exl2exl():
    book = xlrd.open_workbook('dataset1.xlsx')
    sheet1 = book.sheets()[1]

    # nrows = sheet1.nrows
    # ncols = sheet1.ncols

    # row3_values = sheet1.row_values(2)
    # print('第3行值',row3_values)
    # col3_values = sheet1.col_values(2)
    # print('第3列值',col3_values)
    # cell_3_3 = sheet1.cell(2,2).value
    # print('第3行第3列的单元格的值：',cell_3_3)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('test')

    row = 0
    print(sheet1.ncols)
    for i in range(1, sheet1.rows):
        if len(sheet1.row_values(i)) > 1:
            line = sheet1.row_values(i)[-1][1:-1]
            d_l =  line.split("，")
            for j in d_l:
                worksheet.write(row, 0, i)
                worksheet.write(row, 1, j[1:-1])
                worksheet.write(row, 2, sheet1.row_values(i)[1])
            row += 1
    workbook.save('excelwrite.xls')

def json2exl():
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('test')

    with open('./CMeIE_test.json', 'r', encoding='utf-8') as f:
        flag = 1
        lines = f.readlines()
        count = 0
        for line in lines:
            json_data = json.loads(line)
            if flag == 1 and len(json_data['spo_list']) <= 0:
                pass
            else:
                worksheet.write_merge(count, count, 0, 2, json_data['text'])
                count += 1

            for spo in json_data['spo_list']:
                worksheet.write(count, 0, spo['subject'])
                worksheet.write(count, 1, spo['predicate'])
                worksheet.write(count, 2, spo['object']['@value'])
                count += 1

            if flag == 1 and len(json_data['spo_list']) <= 0:
                pass
            else:
                worksheet.write_merge(count, count, 0, 2, ' ')
                count += 1

        workbook.save('a.xls')


def exl2json():
    book = xlrd.open_workbook('test.xlsx')
    table = book.sheets()[0]
    json_data = []
    for i in range(1, table.nrows):
        line = {'text': ''}
        line['text'] = re.sub(r'。+', '。', table.row_values(i)[0].replace(' ','').replace('\n', '。')) 
        json_data.append(line)
    with open('./result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))

def csv2json():
    

    table = pd.read_csv('./CBLUEDatasets/shdx_data_0716/shdx_xiaohua_ptjb.csv')
    json_data = []
    for i, row in table.iterrows():
        line = {'text': ''}
        line['text'] = re.sub(r'。+', '。', row['pttxt'].replace(' ','').replace('\\n', '。'))[1:-1] 
        json_data.append(line)
    with open('./testData/shdx_xiaohua_ptjb.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))        
    
if __name__ == '__main__':
    csv2json()