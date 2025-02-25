# Common Parameters
NUM=6
MAX_LEN=3000
BATCH_SIZE=1
GAS=8
EPOCH=3
LR=1e-4
MODEL_PREFIX="/liuzyai04/thuir/yuebaoqing/LLM"
OUT_DIR_PREFIX="/liuzyai04/thuir/guest/yuebaoqing/hanfei/model"
TRAIN_PATH="/liuzyai04/thuir/yuebaoqing/casegen/data/train.json"
CUR_DIR="/liuzyai04/thuir/yuebaoqing/casegen"

# List of Models
MODEL_NAMES=("hanfei")
for MODEL_NAME in "${MODEL_NAMES[@]}"; do
    MODEL="$MODEL_PREFIX/$MODEL_NAME"
    OUT_DIR="$OUT_DIR_PREFIX/$MODEL_NAME"
    
    # Execute deepspeed command for each model
    deepspeed --include="localhost:0,1,2,3,4,5" --master_port=11469 src/train.py \
        --train_path ${TRAIN_PATH} \
        --max_src $MAX_LEN \
        --max_tar $MAX_LEN \
        --workers ${NUM} \
        --model_name_or_path ${MODEL} \
        --tokenizer_name_or_path ${MODEL} \
        --per_device_train_batch_size $BATCH_SIZE \
        --gradient_accumulation_steps $GAS \
        --num_train_epochs $EPOCH \
        --save_steps 300000 \
        --learning_rate $LR \
        --logging_steps 100000 \
        --output_dir ${OUT_DIR} \
        --deepspeed_config /liuzyai04/thuir/legalaid/llm_frameworks/deepspeed/train_config/zero2_bf16.json
    
    # Convert model weights from zero to fp32
    cd ${OUT_DIR}
    python zero_to_fp32.py . pytorch_model.bin
    cd $CUR_DIR
done