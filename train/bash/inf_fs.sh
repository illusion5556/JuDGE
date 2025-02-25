cd /liuzyai04/thuir/yuebaoqing/casegen/deploy
CUDA_VISIBLE_DEVICES=1 python inf_fs.py --suffix qwen2.5-7B-Instruct --output_path ../output/fewshot/vx/qwen2.5-7B-Instruct-new.json &
CUDA_VISIBLE_DEVICES=2 python inf_fs.py --suffix qwen2.5-3B-Instruct --output_path ../output/fewshot/vx/qwen2.5-3B-Instruct-new.json &
wait
echo "done"
