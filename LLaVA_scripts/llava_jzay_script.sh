#!/bin/bash
#SBATCH --job-name=fineTuneLLaVATest # nom du job
#SBATCH --output=./output/fineTuneLLaVATest%j.out # fichier de sortie (%j = job ID)
#SBATCH --error=./output/fineTuneLLaVATest%j.err # fichier d’erreur (%j = job ID)
#SBATCH --partition=gpu_p2 # demander des GPU a 16 Go de RAM
#SBATCH --nodes=1 # reserver 1 nœud
#SBATCH --ntasks=1 # reserver 4 taches (ou processus)
#SBATCH --gres=gpu:8 # reserver 4 GPU
#SBATCH --cpus-per-task=6 # reserver 10 CPU par tache (et memoire associee)
#SBATCH --time=00:00:40 # temps maximal d’allocation "(HH:MM:SS)"
#SBATCH --qos=qos_gpu-dev # QoS
##SBATCH --qos=qos_gpu-t4 # QoS
#SBATCH --hint=nomultithread # desactiver l’hyperthreading
set -x # activer l’echo des commandes
module load anaconda-py3/2023.09
#module load cuda/12.2.0
conda activate finetune_llava
#module purge
module load pytorch-gpu/py3/2.1.1
export PATH=$WORK/.local/bin:$PATH
export BNB_CUDA_VERSION=118
proxies={"http" : "cache-adm.univ-artois.fr:8080", "https" : "cache-adm.univ-artois.fr:8080"}
srun bash ./finetune_custom.sh # executer son script
