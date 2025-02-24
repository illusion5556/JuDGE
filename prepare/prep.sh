# 每次运行前删除之前生成过的
rm ../data/case_corpus.jsonl
rm ../data/test.json
rm ../data/train.json
rm ../data/qrels_file_test
rm ../data/qrels_file_train

python split.py
echo "split done! "

python gen_case_corpus.py
echo "case corpus generated! "

python gen_dense_train.py
echo "dense_train.json generated! "

python gen_qrels_file.py
echo "qrels_file_test and qrels_file_train generated! "