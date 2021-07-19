#!/usr/bin/env bash

if [ $1 == "test" ];
then
    DATA_DIR="data/input"
    OUTPUT_DIR="data/output"
    FILE_NAME="NER_shdx_guke_ptjb_clean"
    DICT_DIR="data"

    python ./src/main.py \
        --data_dir=${DATA_DIR} \
        --output_dir=${OUTPUT_DIR} \
        --file_name=${FILE_NAME} \
        --dict_dir=${DICT_DIR}
else
    DATA_DIR="data/result_output"
    OUTPUT_DIR="data/output"
    FILE_NAME="NER_shdx_xiaohua_ptjb"
    DICT_DIR="rulesBased/data"

    python ./rulesBased/src/main.py \
        --data_dir=${DATA_DIR} \
        --output_dir=${OUTPUT_DIR} \
        --file_name=${FILE_NAME} \
        --dict_dir=${DICT_DIR}
fi
