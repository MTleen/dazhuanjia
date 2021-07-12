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
MODEL_TYPE="robert"
MODEL_DIR="data/model_data"
MODEL_NAME="chinese_roberta_wwm_ext_pytorch"
OUTPUT_DIR="data/output"
RESULT_OUTPUT_DIR="data/result_output"

MAX_LENGTH=128

echo "Start running"

if [ $# == 0 ]; then
    python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE} \
        --model_dir=${MODEL_DIR} \
        --model_name=${MODEL_NAME} \
        --task_name=${TASK_NAME} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_train \
        --max_length=${MAX_LENGTH} \
        --train_batch_size=16 \
        --eval_batch_size=16 \
        --learning_rate=3e-5 \
        --epochs=5 \
        --warmup_proportion=0.1 \
        --earlystop_patience=3 \
        --logging_steps=200 \
        --save_steps=200 \
        --seed=2021
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