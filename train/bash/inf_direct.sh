cd /liuzyai04/thuir/yuebaoqing/casegen/deploy
CUDA_VISIBLE_DEVICES=0 python inf_direct.py --suffix qwen2.5-7B-Instruct --output_path ../output/qwen2.5-7B-Instruct-direct-new.json &
CUDA_VISIBLE_DEVICES=1 python inf_direct.py --suffix qwen2.5-3B-Instruct --output_path ../output/qwen2.5-3B-Instruct-direct-new.json &
wait