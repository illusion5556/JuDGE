
###
 # @Author: lihaitao
 # @Date: 2023-05-08 17:17:26
 # @LastEditors: Do not edit
 # @LastEditTime: 2023-05-09 13:59:44
 # @FilePath: /lht/ChatGLM_LoRA/lora.sh
### 

# 我用的这份脚本基于lexilaw全量微调出了新的模型
deepspeed --include="localhost:3,4,6,7" --master_port=11469 finetune_lora.py \
    --train_path /liuzyai04/thuir/yuebaoqing/casegen/data/train.json \
    --max_len 3000 \
    --max_input_len 2000 \
    --model_name_or_path /liuzyai04/thuir/yuebaoqing/LLM/LexiLaw/model/LexiLaw \
    --tokenizer_name /liuzyai04/thuir/yuebaoqing/LLM/LexiLaw/model/LexiLaw \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --num_train_epochs 3 \
    --save_steps 90000 \
    --learning_rate 1e-5 \
    --fp16 \
    --remove_unused_columns false \
    --logging_steps 10 \
    --output_dir ../model/full \
    --deepspeed /liuzyai04/thuir/lht/context_learning/LORA/ds_config.json \

cd ../casegen
python inf_ft.py