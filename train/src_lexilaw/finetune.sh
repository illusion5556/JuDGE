NUM=4
deepspeed --include="localhost:3,4,6,7" --master_port=11469 finetune.py \
    --train_path /liuzyai04/thuir/yuebaoqing/casegen/data/train.json \
    --max_len 3000 \
    --max_input_len 2000 \
    --model_name_or_path /liuzyai04/thuir/yuebaoqing/LLM/LexiLaw/model/LexiLaw \
    --tokenizer_name /liuzyai04/thuir/yuebaoqing/LLM/LexiLaw/model/LexiLaw \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --num_train_epochs 3 \
    --save_steps 9000000 \
    --learning_rate 1e-4 \
    --logging_steps 5000000 \
    --output_dir /liuzyai04/thuir/yuebaoqing/LLM/LexiLaw/model/finetune \
    --deepspeed /liuzyai04/thuir/lht/context_learning/LORA/ds_config.json \
    --fp16
