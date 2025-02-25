PRETRAINED_MODEL="../retriever/chinese-roberta-wwm"
PARTS=("train" "test")  # 需要遍历的 PART
CUDA_DEVICE="1" # 定义要使用的是哪块GPU

# build train file
python helpers/build_train_from_ranking.py \
    --tokenizer_name $PRETRAINED_MODEL \
    --random \
    --run_file_train ../retriever/encode/lr/run_file_train \
    --output_train_file reranker_train.json \
    --qry_train_file ../data/train.json \
    --law_data_file ../data/law_corpus.jsonl


# training
CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python run_reranker.py \
    --output_dir train \
    --model_name_or_path $PRETRAINED_MODEL \
    --do_train \
    --train_path reranker_train.json \
    --max_len 512 \
    --fp16 \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 8 \
    --overwrite_output_dir \
    --dataloader_num_workers 8 \

# Define the parts: train and test
for PART in "${PARTS[@]}"; do
    # Build JSON
    mkdir -p result/$PART
    python helpers/topk_text_2_json.py \
        --tokenizer $PRETRAINED_MODEL \
        --save_to result/$PART/all.json \
        --generate_id_to result/$PART/ids.tsv \
        --truncate 200 \
        --q_truncate 512 \
        --qry_train_file ../data/$PART.json \
        --law_data_file ../data/law_corpus.jsonl \
        --run_file_train ../retriever/encode/lr/run_file_$PART

    # Inference
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python run_reranker.py \
        --output_dir score/$PART \
        --model_name_or_path train \
        --tokenizer_name $PRETRAINED_MODEL \
        --do_predict \
        --max_len 512 \
        --fp16 \
        --per_device_eval_batch_size 128 \
        --dataloader_num_workers 32 \
        --pred_path result/$PART/all.json \
        --pred_id_file result/$PART/ids.tsv \
        --rank_score_path score/$PART/score.txt # Specify the path to score.txt

    # Convert to TREC format & evaluate
    python helpers/score_to_tein.py \
        --score_file score/$PART/score.txt \
        --reranker_run_file score/$PART/reranker_run_file_$PART \
        --part $PART

    # TREC evaluation
    ./trec_eval/trec_eval ../data/qrels_file_$PART score/$PART/reranker_run_file_$PART
    ./trec_eval/trec_eval ../data/qrels_file_$PART score/$PART/reranker_run_file_$PART -m recall
done
