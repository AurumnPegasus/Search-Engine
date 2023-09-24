mkdir /scratch/shivansh.s/temp
mkdir /scratch/shivansh.s/invindex/
mkdir -p /scratch/shivansh.s/invindex/titles
python3 read_data.py /scratch/shivansh.s/enwiki-20220820-pages-articles-multistream.xml /scratch/shivansh.s/invindex/ /scratch/shivansh.s/indexstat.txt
python3 invertindex.py /scratch/shivansh.s/invindex/
rm -rf /scratch/shivansh.s/temp/
