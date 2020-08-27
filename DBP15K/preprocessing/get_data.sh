mkdir raw_data
mkdir processed_data
mkdir processed_data/clean
mkdir processed_data/embeddings
mkdir processed_data/aligned_embeddings
mkdir processed_data/graph_data
mkdir processed_data/dictionaries 

wget http://ws.nju.edu.cn/jape/data/DBP15k.tar.gz -P raw_data
tar -C raw_data --wildcards --strip=2 -zxvf raw_data/DBP15k.tar.gz DBP15k/fr_en/*

rm raw_data/DBP15k.tar.gz
