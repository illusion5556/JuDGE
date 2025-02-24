# 运行前，请将sailer下载到当前路径下

CUDA_DEVICE="1" # 定义要使用的是哪块GPU
Q_MAX_LEN=512 # 如要调整，不可超过512
P_MAX_LEN=200 # 如要调整，不可超过512
MODEL_NAME="sailer"
PART="test"

# encode corpus
CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
    --output_dir encode/$MODEL_NAME \
    --tokenizer_name $MODEL_NAME \
    --model_name_or_path $OUTPUT_MODEL_PATH \
    --fp16 \
    --per_device_eval_batch_size 128 \
    --encode_in_path ../data/case_corpus.jsonl \
    --encoded_save_path encode/$MODEL_NAME/corpus_$PART.pt \
    --p_max_len $P_MAX_LEN

echo "Encoding corpus finished for $MODEL_NAME with $PART!"
echo

# encode queries
CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
    --output_dir encode/$MODEL_NAME \
    --tokenizer_name $MODEL_NAME \
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

# sailer 不评测效果。