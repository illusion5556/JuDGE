cd /home/ubuntu/JuDGE/train/deploy
# CUDA_VISIBLE_DEVICES=0 python inf_mrag.py --suffix qwen2.5-7B-Instruct --output_path ../output/mrag/qwen2.5-7B-Instruct.json &
# CUDA_VISIBLE_DEVICES=2 python inf_mrag.py --suffix qwen2.5-7B --output_path ../output/mrag/qwen2.5-7B.json &
# CUDA_VISIBLE_DEVICES=3 python inf_mrag.py --suffix qwen2.5-3B-Instruct --output_path ../output/mrag/qwen2.5-3B-Instruct.json &
# CUDA_VISIBLE_DEVICES=7 python inf_mrag.py --suffix qwen2.5-3B --output_path ../output/mrag/qwen2.5-3B.json &
# wait
# echo "All inference executed."

CUDA_VISIBLE_DEVICES=0 python inf_mrag.py --suffix mragsft_multi_bt_p1 --output_path ../../output/mrag_rl --model_path /home/ubuntu/weight/wubinglin/verl/hf/judge/&
# CUDA_VISIBLE_DEVICES=1 python inf_mrag.py --suffix multi_mb_bt_p1 --output_path ../../output/mrag_rl --model_path /home/ubuntu/weight/wubinglin/verl/hf/judge/&
# CUDA_VISIBLE_DEVICES=2 python inf_mrag.py --suffix 7b_ins_mrag_ep4 --output_path ../../output/mrag --model_path /home/ubuntu/weight/wubinglin/judge_ft/full_sft/&
# CUDA_VISIBLE_DEVICES=4 python inf_mrag.py --suffix 3b_ins_mrag_ep4 --output_path ../../output/mrag --model_path /home/ubuntu/weight/wubinglin/judge_ft/full_sft/&
# CUDA_VISIBLE_DEVICES=3 python inf_mrag.py --suffix Qwen2.5-3B-Instruct --output_path ../../output/mrag --model_path /home/ubuntu/weight/wubinglin/judge_ft/full_sft/&
# CUDA_VISIBLE_DEVICES=4 python inf_mrag.py --suffix qwen2.5-3B --output_path ../output/mrag/v7/qwen2.5-3B.json &
wait
echo "done"