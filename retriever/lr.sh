# 运行前，请将chinese-roberta-wwm下载到当前路径下，并在项目根路径下配置好trec_eval

CUDA_DEVICE="1" # 定义要使用的是哪块GPU
PRETRAINED_MODEL="chinese-roberta-wwm"
OUTPUT_MODEL_PATH="train/model"
SAVE_STEPS=1437
LEARNING_RATE=5e-6
EPOCH=10
BATCH_SIZE=6
DATALOADER_NUM_WORKERS=2
Q_MAX_LEN=512 # 最大512
P_MAX_LEN=200 # 最大512
MODEL_NAME="lr"  # 只设置 MODEL_NAME 为 "lr"
PARTS=("train" "test")  # 需要遍历的 PART

# 遍历 PARTS
for PART in "${PARTS[@]}"; do
    echo "Running with MODEL_NAME=$MODEL_NAME and PART=$PART"

    # 仅当 MODEL_NAME 是 "lr" 且 PART 是 "train" 时才执行训练
    if ["$PART" == "train" ]; then
        # train dense-retriever model
        CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.train \
            --do_train \
            --train_dir train \
            --output_dir $OUTPUT_MODEL_PATH \
            --tokenizer_name $PRETRAINED_MODEL \
            --model_name_or_path $PRETRAINED_MODEL \
            --save_steps $SAVE_STEPS \
            --per_device_train_batch_size $BATCH_SIZE \
            --learning_rate $LEARNING_RATE \
            --num_train_epochs $EPOCH \
            --dataloader_num_workers $DATALOADER_NUM_WORKERS \
            --overwrite_output_dir \
            --q_max_len $Q_MAX_LEN \
            --p_max_len $P_MAX_LEN \
            --fp16

        echo "Training finished!"
        echo
    fi

    # encode corpus
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
        --output_dir encode/$MODEL_NAME \
        --tokenizer_name $PRETRAINED_MODEL \
        --model_name_or_path $OUTPUT_MODEL_PATH \
        --fp16 \
        --per_device_eval_batch_size 128 \
        --encode_in_path ../data/law_corpus.jsonl \
        --encoded_save_path encode/$MODEL_NAME/corpus_$PART.pt \
        --p_max_len $P_MAX_LEN

    echo "Encoding corpus finished for $MODEL_NAME with $PART!"
    echo

    # encode queries
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
        --output_dir encode/$MODEL_NAME \
        --tokenizer_name $PRETRAINED_MODEL \
        --model_name_or_path $OUTPUT_MODEL_PATH \
        --fp16 \
        --per_device_eval_batch_size 128 \
        --encode_in_path ../data/$PART.json \
        --encoded_save_path encode/$MODEL_NAME/queries_$PART.pt \
        --q_max_len $Q_MAX_LEN

    echo "Encoding queries finished for $MODEL_NAME with $PART!"
    echo

    # faiss_retriever
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.faiss_retriever \
        --query_reps encode/$MODEL_NAME/queries_$PART.pt \
        --passage_reps encode/$MODEL_NAME/corpus_$PART.pt \
        --depth 100 \
        --batch_size -1 \
        --save_text \
        --save_ranking_to encode/$MODEL_NAME/rank_$PART.tsv

    echo "Retrieving finished for $MODEL_NAME with $PART!"
    echo

    python rank2trec.py \
        --rank_txt_file encode/$MODEL_NAME/rank_$PART.txt \
        --run_file encode/$MODEL_NAME/run_file_$PART \
        --model_name $MODEL_NAME \
        --part $PART

    # 定义 qrels 和 results 文件路径
    qrels_file="../data/qrels_file_$PART"
    results_file="encode/$MODEL_NAME/run_file_$PART"

    ./../trec_eval/trec_eval $qrels_file $results_file
    ./../trec_eval/trec_eval -m recall.5 $qrels_file $results_file
    ./../trec_eval/trec_eval -m recall.10 $qrels_file $results_file
    ./../trec_eval/trec_eval -m recall.100 $qrels_file $results_file

    echo "Finished evaluation for $MODEL_NAME with $PART!"
    echo
done
