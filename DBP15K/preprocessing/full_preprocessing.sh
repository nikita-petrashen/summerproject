# download data
./get_data.sh
# clean raw data
python clean.py
# get monolingual fasttext embeddings
./fasttext.sh
# align embeddings to the same space
./muse.sh
# prepare input data for DGMC
python graph_preparation.py
# prepare input data for s-GWL
python sgwl_preprocessing.py