# Common Parameters
NUM=5
MAX_LEN=3000
BATCH_SIZE=1
GAS=8
EPOCH=3
LR=1e-4
MODEL_PREFIX="/liuzyai04/thuir/yuebaoqing/LLM"
OUT_DIR_PREFIX="/liuzyai04/thuir/yuebaoqing/casegen/model/finetune/v4"
TRAIN_PATH="/liuzyai04/thuir/yuebaoqing/casegen/Data/train.json"
CUR_DIR="/liuzyai04/thuir/yuebaoqing/casegen"

# # List of Models
# MODEL_NAMES=("qwen2.5-7B" "qwen2.5-7B-Instruct" "qwen2.5-3B-Instruct" "qwen2.5-3B")
# for MODEL_NAME in "${MODEL_NAMES[@]}"; do
#     MODEL="$MODEL_PREFIX/$MODEL_NAME"
#     OUT_DIR="$OUT_DIR_PREFIX/$MODEL_NAME"
    
#     # Execute deepspeed command for each model
#     deepspeed --include="localhost:0,1,2,3,7" --master_port=11469 src/train.py \
#         --train_path ${TRAIN_PATH} \
#         --max_src $MAX_LEN \
#         --max_tar $MAX_LEN \
#         --workers ${NUM} \
#         --model_name_or_path ${MODEL} \
#         --tokenizer_name_or_path ${MODEL} \
#         --per_device_train_batch_size $BATCH_SIZE \
#         --gradient_accumulation_steps $GAS \
#         --num_train_epochs $EPOCH \
#         --save_steps 300000 \
#         --learning_rate $LR \
#         --logging_steps 100000 \
#         --output_dir ${OUT_DIR} \
#         --deepspeed_config /liuzyai04/thuir/legalaid/llm_frameworks/deepspeed/train_config/zero2_bf16.json
    
#     # Convert model weights from zero to fp32
#     cd ${OUT_DIR}
#     python zero_to_fp32.py . pytorch_model.bin
#     cd $CUR_DIR
# done


cd /liuzyai04/thuir/yuebaoqing/casegen/deploy
CUDA_VISIBLE_DEVICES=3 python inf.py --suffix qwen2.5-7B-Instruct --output_path ../output/finetune/vx/qwen2.5-7B-Instruct.json &
CUDA_VISIBLE_DEVICES=5 python inf.py --suffix qwen2.5-7B --output_path ../output/finetune/vx/qwen2.5-7B.json &
CUDA_VISIBLE_DEVICES=6 python inf.py --suffix qwen2.5-3B-Instruct --output_path ../output/finetune/vx/qwen2.5-3B-Instruct.json &
CUDA_VISIBLE_DEVICES=7 python inf.py --suffix qwen2.5-3B --output_path ../output/finetune/vx/qwen2.5-3B.json &
wait
echo "Finetune inference executed."

# CUDA_VISIBLE_DEVICES=0 python inf_multi.py --suffix qwen2.5-7B-Instruct --output_path ../output/multi/v4/qwen2.5-7B-Instruct.json &
# CUDA_VISIBLE_DEVICES=1 python inf_multi.py --suffix qwen2.5-7B --output_path ../output/multi/v4/qwen2.5-7B.json &
# CUDA_VISIBLE_DEVICES=2 python inf_multi.py --suffix qwen2.5-3B-Instruct --output_path ../output/multi/v4/qwen2.5-3B-Instruct.json &
# CUDA_VISIBLE_DEVICES=3 python inf_multi.py --suffix qwen2.5-3B --output_path ../output/multi/v4/qwen2.5-3B.json &
# wait
# echo "Multi inference executed."

# CUDA_VISIBLE_DEVICES=3 python inf.py --suffix qwen2.5-7B-Instruct --output_path ../output/finetune/vx/qwen2.5-7B-Instruct.json

# CUDA_VISIBLE_DEVICES=3 python inf.py --suffix qwen2.5-7B-Instruct --output_path ../output/finetune/vx/qwen2.5-7B-Instruct.json --dataset_path ../data/spl_test.json