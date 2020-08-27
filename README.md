# summerproject
This repo is dedicated to my Skoltech Summer Immersion at Huawei. The repository is split in two parts: one is dedicated to experiments with DBP15K dataset, another part is dedicated to my experiments with new biomedical dataset.

## DBP15K
To get data and perform preprocessing run preprocessing/full_preprocessing.sh \ 
To run experiments you will need to install torch-geometric, https://github.com/rusty1s/deep-graph-matching-consensus and https://github.com/HongtengXu/s-gwl. \ 
dgmc_experiments.sh will run DGMC hyperparameters robustness test. \ 
DGMC_dbp15k_my.py will run DGMC on my version of the DBP15K dataset. \ 
hungarian notebooks contain experments with Hungarian algorithm on my and torch-geometric versions of DBP15K \
Before running experiments with s-GWL you will need to copy the respective files to your s-GWL directory and change the respective variables which contain paths to data and results folders. \ 

## Biomedical data
### TODO
