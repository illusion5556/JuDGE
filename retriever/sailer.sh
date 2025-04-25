# Define the GPU to use
CUDA_DEVICE="5" 
Q_MAX_LEN=512 # Maximum length for queries, should not exceed 512
P_MAX_LEN=200 # Maximum length for passages, should not exceed 512
MODEL_NAME="sailer"

# Iterate over both 'train' and 'test' parts
for PART in train test; do
    mkdir -p encode/$MODEL_NAME

    # Encode corpus
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
        --output_dir encode/$MODEL_NAME \
        --tokenizer_name $MODEL_NAME \
        --model_name_or_path $MODEL_NAME \
        --fp16 \
        --per_device_eval_batch_size 128 \
        --encode_in_path ../data/case_corpus.jsonl \
        --encoded_save_path encode/$MODEL_NAME/corpus_$PART.pt \
        --p_max_len $P_MAX_LEN

    echo "Encoding corpus finished for $MODEL_NAME with $PART!"
    echo

    # Encode queries
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python -m dense.driver.encode \
        --output_dir encode/$MODEL_NAME \
        --tokenizer_name $MODEL_NAME \
        --model_name_or_path $MODEL_NAME \
        --fp16 \
        --per_device_eval_batch_size 128 \
        --encode_in_path ../data/$PART.json \
        --encoded_save_path encode/$MODEL_NAME/queries_$PART.pt \
        --q_max_len $Q_MAX_LEN

    echo "Encoding queries finished for $MODEL_NAME with $PART!"
    echo

    # Faiss retriever
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
        --rank_txt_file encode/$MODEL_NAME/rank_$PART.tsv \
        --run_file encode/$MODEL_NAME/run_file_$PART \
        --model_name $MODEL_NAME \
        --part $PART
done

# Since the sailer model does not require evaluation, this step is skipped.