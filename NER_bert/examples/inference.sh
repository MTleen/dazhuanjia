#!/usr/bin/env bash
DATA_DIR="CBLUEDatasets"

TASK_NAME_EE="ee"
MODEL_TYPE_EE="roberta"
MODEL_NAME_EE="roberta-wwm-ext"

TASK_NAME_IE="ie"
MODEL_TYPE_IE="bert"
MODEL_NAME_IE="robert_base"

MODEL_DIR="data/model_data"
OUTPUT_DIR="data/output"
RESULT_OUTPUT_DIR="data/result_output"

MAX_LENGTH=128



echo "Start running EE"
# EE
python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE_EE} \
        --model_name=${MODEL_NAME_EE} \
        --model_dir=${MODEL_DIR} \
        --task_name=${TASK_NAME_EE} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_predict \
        --max_length=${MAX_LENGTH} \
        --eval_batch_size=32 \
        --seed=2021

echo "Start running IE"
# IE
python baselines/inference.py \
    --data_dir=${DATA_DIR} \
    --model_type=${MODEL_TYPE_IE} \
    --model_name=${MODEL_NAME_IE} \
    --model_dir=${MODEL_DIR} \
    --task_name=${TASK_NAME_IE} \
    --output_dir=${OUTPUT_DIR} \
    --result_output_dir=${RESULT_OUTPUT_DIR} \
    --max_length=${MAX_LENGTH} \
    --eval_batch_size=32
