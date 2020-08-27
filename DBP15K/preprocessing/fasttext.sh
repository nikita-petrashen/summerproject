mkdir fasttext_models

# getting fasttext models for English and French
wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip -P fasttext_models
wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.fr.zip -P fasttext_models

# unzipping .bin files to fasttext_models
unzip -j "fasttext_models/wiki.fr.zip" "wiki.fr.bin" -d "fasttext_models"
rm fasttext_models/wiki.fr.zip
unzip -j "fasttext_models/wiki.en.zip" "wiki.en.bin" -d "fasttext_models"
rm fasttext_models/wiki.en.zip

# preparing fastText
git clone https://github.com/facebookresearch/fastText.git
cd fastText
mkdir build && cd build && cmake ..
make && make install
cd ../..

# MUSE needs the first line of input files to contain the number of words and embeddings dimensionality (300)
echo `wc -l < processed_data/clean/en_entities` 300 > processed_data/embeddings/en_entities.vec
cat processed_data/clean/en_entities | ./fastText/fasttext print-word-vectors fasttext_models/wiki.en.bin >> processed_data/embeddings/en_entities.vec

echo `wc -l < processed_data/clean/en_relations` 300 > processed_data/embeddings/en_relations.vec
cat processed_data/clean/en_relations | ./fastText/fasttext print-word-vectors fasttext_models/wiki.en.bin >> processed_data/embeddings/en_relations.vec

echo `wc -l < processed_data/clean/fr_entities` 300 > processed_data/embeddings/fr_entities.vec
cat processed_data/clean/fr_entities | ./fastText/fasttext print-word-vectors fasttext_models/wiki.fr.bin >> processed_data/embeddings/fr_entities.vec

echo `wc -l < processed_data/clean/fr_relations` 300 > processed_data/embeddings/fr_relations.vec
cat processed_data/clean/fr_relations | ./fastText/fasttext print-word-vectors fasttext_models/wiki.fr.bin >> processed_data/embeddings/fr_relations.vec