git clone https://github.com/facebookresearch/MUSE

# recommended dependency for fast nearest-neighbor search
conda install faiss-gpu -c pytorch

# get data for embeddings evaluation
chmod 777 ./MUSE/data/get_evaluation.sh
./MUSE/data/get_evaluation.sh

# align entities' embeddings
python MUSE/unsupervised.py --src_lang fr --tgt_lang en --src_emb processed_data/embeddings/fr_entities.vec --tgt_emb processed_data/embeddings/en_entities.vec --n_refinement 5 --exp_path processed_data/aligned_embeddings/entities --exp_id 1 --dis_most_frequent 50000

# align relations' embeddings
python MUSE/unsupervised.py --src_lang fr --tgt_lang en --src_emb processed_data/embeddings/fr_relations.vec --tgt_emb processed_data/embeddings/en_relations.vec --n_refinement 5 --exp_path processed_data/aligned_embeddings/relations --exp_id 1 --dis_most_frequent 1200 