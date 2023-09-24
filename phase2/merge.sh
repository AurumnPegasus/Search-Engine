#!/bin/bash
#SBATCH -c 10
#SBATCH -A research
#SBATCH -w gnode063
#SBATCH --mem-per-cpu 2G
#SBATCH --time 4-00:00:00
#SBATCH --output logs/ire.log
#SBATCH --mail-user shivansh.s@research.iiit.ac.in
#SBATCH --mail-type ALL
#SBATCH --job-name ire_lang

python3 invertindex.py /scratch/shivansh.s/invindex/
