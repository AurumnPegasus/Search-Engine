#!/bin/bash
#SBATCH -c 35
#SBATCH -A research
#SBATCH --mem-per-cpu 2G
#SBATCH --time 4-00:00:00
#SBATCH --output logs/final.log
#SBATCH --mail-user shivansh.s@research.iiit.ac.in
#SBATCH --mail-type ALL
#SBATCH --job-name ire

mkdir -p /scratch/shivansh.s/
scp -r shivansh.s@ada:/share1/shivansh.s/enwiki-20220820-pages-articles-multistream.xml.bz2 /scratch/shivansh.s/
rm -rf /scratch/shivansh.s/temp
rm -rf /scratch/shivansh.s/invindex
mkdir -p /scratch/shivansh.s/temp/
mkdir -p /scratch/shivansh.s/invindex/
mkdir -p /scratch/shivansh.s/invindex/titles
bzip2 -d /scratch/shivansh.s/enwiki-20220820-pages-articles-multistream.xml.bz2
python3 read_data.py /scratch/shivansh.s/enwiki-20220820-pages-articles-multistream.xml /scratch/shivansh.s/invindex/ /scratch/shivansh.s/indexstat.txt
python3 invertindex.py /scratch/shivansh.s/invindex/
