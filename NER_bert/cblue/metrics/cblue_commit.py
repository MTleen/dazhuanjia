import os
import json
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


def ee_commit_prediction(dataset, preds, output_dir):
    orig_text = dataset.orig_text

    pred_result = []
    pred_res_dict = {}
    for item in zip(orig_text, preds):
        hash_val = item[0]['hash']
        tmp_dict = {'text': item[0]['text'], 'entities': item[1]}
        if hash_val in pred_res_dict.keys():
            pred_res_dict[hash_val]['text'] += tmp_dict['text']
            pred_res_dict[hash_val]['entities'] += tmp_dict['entities']
        else:
            pred_res_dict[hash_val] = tmp_dict
    # pred_result.append(tmp_dict)
    pred_result = list(pred_res_dict.values())
    with open(os.path.join(output_dir, 'CMeEE_test.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pred_result, indent=2, ensure_ascii=False))

    # 输出主客体
    re_res = {'text':'', 'sub_list': [], 'obj_list': []}
    for l in pred_result:
        re_res['text'] = l['text']
        for e in l['entities']:
            re_res['sub_list'].append(e['entity'])
            re_res['obj_list'].append(e['entity'])

    with open(os.path.join(output_dir, 'NER_test1.json'),
              'w',
              encoding='utf-8') as f:
        f.write(json.dumps(re_res, indent=2, ensure_ascii=False))


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
