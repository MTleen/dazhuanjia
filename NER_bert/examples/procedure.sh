DATA_DIR="CBLUEDatasets"

TASK_NAME="ee"
MODEL_TYPE="roberta"
MODEL_DIR="data/model_data"
MODEL_NAME="roberta-wwm-ext"
OUTPUT_DIR="data/output"
RESULT_OUTPUT_DIR="data/result_output"

MAX_LENGTH=128
echo "开始实体识别 shdx_guke_fangdajb.json"
nohup python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE} \
        --model_name=${MODEL_NAME} \
        --model_dir=${MODEL_DIR} \
        --test_file_path="shdx_guke_fangdajb.json" \
        --task_name=${TASK_NAME} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_predict \
        --max_length=${MAX_LENGTH} \
        --eval_batch_size=32 \
        --seed=2021 > log/predict_guke_fangdajb.log 2>&1 &

echo "开始实体识别 shdx_xiaohua_fangdajb.json"
nohup python baselines/run_classifier.py \
        --data_dir=${DATA_DIR} \
        --model_type=${MODEL_TYPE} \
        --model_name=${MODEL_NAME} \
        --model_dir=${MODEL_DIR} \
        --test_file_path="shdx_xiaohua_fangdajb.json" \
        --task_name=${TASK_NAME} \
        --output_dir=${OUTPUT_DIR} \
        --result_output_dir=${RESULT_OUTPUT_DIR} \
        --do_predict \
        --max_length=${MAX_LENGTH} \
        --eval_batch_size=32 \
        --seed=2021 > log/predict_xiaohua_fangdajb.log 2>&1 &

# echo "开始实体识别 shdx_xiaohua_ptjb.json"
# nohup python baselines/run_classifier.py \
#         --data_dir=${DATA_DIR} \
#         --model_type=${MODEL_TYPE} \
#         --model_name=${MODEL_NAME} \
#         --model_dir=${MODEL_DIR} \
#         --test_file_path="shdx_xiaohua_ptjb.json" \
#         --task_name=${TASK_NAME} \
#         --output_dir=${OUTPUT_DIR} \
#         --result_output_dir=${RESULT_OUTPUT_DIR} \
#         --do_predict \
#         --max_length=${MAX_LENGTH} \
#         --eval_batch_size=32 \
#         --seed=2021 > log/predict3.log 2>&1 &