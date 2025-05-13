cd /home/ubuntu/JuDGE/train/deploy
CUDA_VISIBLE_DEVICES=3 python inf_fs.py --suffix Qwen2.5-7B-Instruct --output_path ../../output/fs &
CUDA_VISIBLE_DEVICES=4 python inf_fs.py --suffix Qwen2.5-3B-Instruct --output_path ../../output/fs &
wait
echo "done"
