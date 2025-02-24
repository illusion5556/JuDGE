GEN_FILE="generated.jsonl" # 替换成你的gen_file
EXP_FILE="expected.jsonl"
python calc.py \
    --gen_file $GEN_FILE \
    --exp_file $EXP_FILE
python calc_rel.py \
    --gen_file $GEN_FILE \
    --exp_file $EXP_FILE