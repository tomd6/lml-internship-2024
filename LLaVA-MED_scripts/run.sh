#!/bin/bash

torchrun --nnodes=1 --nproc_per_node=2 \
    llava/train/train.py \
    --model_name_or_path llava-hf/llava-v1.6-mistral-7b-hf \
     --data_path /gpfsscratch/rech/iqc/commun/st/datasets/rt1_llava_full_dataset/train/dataset.json \
    --image_folder /gpfsscratch/rech/iqc/commun/st/datasets/rt1_llava_full_dataset/images/ \
    --vision_tower openai/clip-vit-large-patch14 \
    --tune_mm_mlp_adapter True \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end \
    --fp16 True \
    --output_dir ./checkpoints/llava-mistral \
    --num_train_epochs 3 \
    --per_device_train_batch_size 256 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 200 \
    --save_total_limit 1 \
    --learning_rate 2e-3 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --fp16 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True \
    --report_to none
