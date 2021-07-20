import os
import json
import xlrd
import xlwt
import numpy as np


def sts_commit_prediction(dataset, preds, output_dir, id2label):
    text1 = dataset.text1
    text2 = dataset.text2
    label = preds
    ids = dataset.ids
    category = dataset.category

    pred_result = []
    for item in zip(ids, text1, text2, label, category):
        tmp_dict = {'id': item[0], 'text1': item[1], 'text2': item[2],
                    'label': id2label[item[3]], 'category': item[4]}
        pred_result.append(tmp_dict)
    with open(os.path.join(output_dir, 'CHIP-STS_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))


def qic_commit_prediction(dataset, preds, output_dir, id2label):
    text1 = dataset.text
    label = preds
    ids = dataset.ids

    pred_result = []
    for item in zip(ids, text1, label):
        tmp_dict = {'id': item[0], 'query': item[1],
                    'label': id2label[item[2]]}
        pred_result.append(tmp_dict)
    with open(os.path.join(output_dir, 'KUAKE-QIC_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))


def qtr_commit_prediction(dataset, preds, output_dir, id2label):
    text1 = dataset.text1
    text2 = dataset.text2
    label = preds
    ids = dataset.ids

    pred_result = []
    for item in zip(ids, text1, text2, label):
        tmp_dict = {'id': item[0], 'text1': item[1], 'text2': item[2],
                    'label': id2label[item[3]]}
        pred_result.append(tmp_dict)
    with open(os.path.join(output_dir, 'KUAKE-QTR_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))


def qqr_commit_prediction(dataset, preds, output_dir, id2label):
    text1 = dataset.text1
    text2 = dataset.text2
    label = preds
    ids = dataset.ids

    pred_result = []
    for item in zip(ids, text1, text2, label):
        tmp_dict = {'id': item[0], 'query1': item[1], 'query2': item[2],
                    'label': id2label[item[3]]}
        pred_result.append(tmp_dict)
    with open(os.path.join(output_dir, 'KUAKE-QQR_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))


def ctc_commit_prediction(dataset, preds, output_dir, id2label):
    text1 = dataset.texts
    label = preds
    ids = dataset.ids

    pred_result = []
    for item in zip(ids, text1, label):
        tmp_dict = {'id': item[0], 'text': "".join(item[1]),
                    'label': id2label[item[2]]}
        pred_result.append(tmp_dict)
    with open(os.path.join(output_dir, 'CHIP-CTC_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))


def ee_commit_prediction(dataset, preds, output_dir, file_name):
    orig_text = dataset.orig_text
    #  原始语料无需分片
    pred_result_seg = []
    for item in zip(orig_text, preds):
        tmp_dict = {'orig_info': item[0], 'entities': item[1]}
        pred_result_seg.append(tmp_dict)
    
    print('输出各子句 NER json')
    with open(os.path.join(output_dir, 'seg_NER_' + file_name), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result_seg, indent=2, ensure_ascii=False))
    
    # 原始语料分片
    pred_result = []
    pred_res_dict = {}
    for item in zip(orig_text, preds):
        hash_val = item[0]['hash']
        tmp_dict = {'text': item[0]['text'], 'entities': item[1]}
        # tmp_dict = {'text': item[0]['origin_text'], 'entities': item[1]}
        if hash_val in pred_res_dict.keys():
            # 还原实体 idx
            if len(tmp_dict['entities']) > 0:
                for e in tmp_dict['entities']:
                    e['start_idx'] += len(pred_res_dict[hash_val]['text']) + 1
                    e['end_idx'] += len(pred_res_dict[hash_val]['text']) + 1

            pred_res_dict[hash_val]['text'] += tmp_dict['text']
            pred_res_dict[hash_val]['entities'] += tmp_dict['entities']
        else:
            pred_res_dict[hash_val] = tmp_dict
    # # 将最终文本替换成原始文本
    # for item in orig_text:
    #     pred_res_dict[item['hash']]['text'] = item['origin_text']
    # pred_result.append(tmp_dict)
    pred_result = list(pred_res_dict.values())


    print('输出 NER json')
    with open(os.path.join(output_dir, 'NER_' + file_name), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))

    # 输出主客体
    with open(os.path.join(output_dir, 'SubObj_' + file_name),
              'w',
              encoding='utf-8') as f:
        for l in pred_result:
            re_res = {'text':'', 'sub_list': [], 'obj_list': []}
            re_res['text'] = l['text']
            for e in l['entities']:
                if e['type'] == 'dis':
                    re_res['sub_list'].append(e['entity'])
                else:
                    re_res['obj_list'].append(e['entity'])
            f.write(json.dumps(re_res, ensure_ascii=False) + '\n')

    # 输出 excel
    print('输出 NER excel')
    json2xls('NER_' + os.path.splitext(file_name)[0], pred_result)

def json2xls(file_name, lines):
    # print(lines)
    workbook = xlwt.Workbook()

    RESULT_PATH = './data/result_output'
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

    flag = 0
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
        count = 1
        for j, value in enumerate(['原始病历', '实体类型', '医疗实体']): #写表头 
            #print(value) 
            worksheet.write(0, j, value)
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


def cdn_commit_prediction(text, preds, num_preds, recall_labels, recall_scores, output_dir, id2label):
    text1 = text

    pred_result = []
    active_indices = (preds >= 0.5)
    for text, active_indice, pred, num, recall_label, recall_score in zip(text1, active_indices, preds, num_preds, recall_labels, recall_scores):
        tmp_dict = {'text': text, 'normalized_result': []}

        final_pred = pred[active_indice]
        recall_score = recall_score[active_indice]
        recall_label = recall_label[active_indice]

        if len(final_pred):
            final_score = (recall_score / 2 + final_pred) / 2
            final_score = np.argsort(final_score)[::-1]
            recall_label = recall_label[final_score]

            num = num + 1
            ji, ban, dou = text.count("及"), text.count("伴"), text.count(";")
            if (ji + ban + dou + 1) > num:
                num = ji + ban + dou + 1
            if num == 1:
                tmp_dict['normalized_result'].append(recall_label[0])
            elif num == 2:
                tmp_dict['normalized_result'].extend(recall_label[:2].tolist())
            else:
                sum_ = max((ji + ban + dou + 1), num, 3)
                tmp_dict['normalized_result'].extend(recall_label[:sum_].tolist())
            tmp_dict['normalized_result'] = [id2label[idx] for idx in tmp_dict['normalized_result']]

        if len(tmp_dict['normalized_result']) == 0:
            tmp_dict['normalized_result'] = [text]
        tmp_dict['normalized_result'] = "##".join(tmp_dict['normalized_result'])
        pred_result.append(tmp_dict)

    with open(os.path.join(output_dir, 'CHIP-CDN_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))
