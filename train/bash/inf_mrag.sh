cd /home/ubuntu/JuDGE/train/deploy
# CUDA_VISIBLE_DEVICES=0 python inf_mrag.py --suffix qwen2.5-7B-Instruct --output_path ../output/mrag/qwen2.5-7B-Instruct.json &
# CUDA_VISIBLE_DEVICES=2 python inf_mrag.py --suffix qwen2.5-7B --output_path ../output/mrag/qwen2.5-7B.json &
# CUDA_VISIBLE_DEVICES=3 python inf_mrag.py --suffix qwen2.5-3B-Instruct --output_path ../output/mrag/qwen2.5-3B-Instruct.json &
# CUDA_VISIBLE_DEVICES=7 python inf_mrag.py --suffix qwen2.5-3B --output_path ../output/mrag/qwen2.5-3B.json &
# wait
# echo "All inference executed."

CUDA_VISIBLE_DEVICES=0 python inf_mrag.py --suffix Qwen2.5-7B-Instruct --output_path ../../output/mrag &
CUDA_VISIBLE_DEVICES=1 python inf_mrag.py --suffix Qwen2.5-7B --output_path ../../output/mrag &
CUDA_VISIBLE_DEVICES=2 python inf_mrag.py --suffix Qwen2.5-3B-Instruct --output_path ../../output/mrag &
# CUDA_VISIBLE_DEVICES=4 python inf_mrag.py --suffix qwen2.5-3B --output_path ../output/mrag/v7/qwen2.5-3B.json &
wait
echo "done"