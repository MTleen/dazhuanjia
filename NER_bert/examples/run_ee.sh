#!/usr/bin/env bash
###
 # @Description: 
 # @Author: Shengxiang Hu
 # @Github: https://github.com/MTleen
 # @Date: 2021-06-20 14:30:56
 # @LastEditors: Shengxiang Hu
 # @LastEditTime: 2021-07-07 16:25:36
 # @FilePath: /2021-06-20 CBLUE/examples/run_ee.sh
### 
DATA_DIR="CBLUEDatasets"

TASK_NAME="ee"
MODEL_TYPE="roberta"
MODEL_DIR="data/model_data"
MODEL_NAME="roberta-wwm-ext"
OUTPUT_DIR="data/output"
RESULT_OUTPUT_DIR="data/result_output"

MAX_LENGTH=128

echo "Start running"

if [ $# == 0 ]; then
    nohup python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE} \
        --model_dir=${MODEL_DIR} \
        --model_name=${MODEL_NAME} \
        --task_name=${TASK_NAME} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_train \
        --max_length=${MAX_LENGTH} \
        --train_batch_size=32 \
        --eval_batch_size=32 \
        --learning_rate=3e-5 \
        --epochs=10 \
        --warmup_proportion=0.1 \
        --earlystop_patience=50 \
        --logging_steps=200 \
        --save_steps=200 \
        --seed=2021 > log/train.log 2>&1 &
elif [ $1 == "predict" ]; then
    python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE} \
        --model_name=${MODEL_NAME} \
        --model_dir=${MODEL_DIR} \
        --task_name=${TASK_NAME} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_predict \
        --max_length=${MAX_LENGTH} \
        --eval_batch_size=32 \
        --seed=2021
fi