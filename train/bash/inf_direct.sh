cd /home/ubuntu/JuDGE/train/deploy
CUDA_VISIBLE_DEVICES=1 python inf_direct.py --suffix Qwen2.5-7B-Instruct --output_path ../../output/direct &
CUDA_VISIBLE_DEVICES=2 python inf_direct.py --suffix Qwen2.5-3B-Instruct --output_path ../../output/direct &
wait