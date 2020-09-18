mkdir pubmed
mkdir pubmed/raw
mkdir pubmed/processed
mkdir opentargets
mkdir opentargets/raw
mkdir opentargets/processed
mkdir dictionaries 
mkdir graph_data
mkdir word2vec 

# this file I got from Elena T.
mv disease_efo_ids.tsv pubmed/raw/disease_efo_ids.tsv

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=14YrlOGd1NdDn0XD-Yat4bbq3lRv1EyqR' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=14YrlOGd1NdDn0XD-Yat4bbq3lRv1EyqR" -O pubmed/raw/2019_merged_json_fixed.zip && rm -rf /tmp/cookies.txt

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1tVYRh3bQ9TzpAlVPLVii4drafzC2EUCB' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1tVYRh3bQ9TzpAlVPLVii4drafzC2EUCB" -O pubmed/raw/gene_meta.tsv && rm -rf /tmp/cookies.txt

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1guHxBbUksuDx58zKh8o0d0dgs7klotFT' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1guHxBbUksuDx58zKh8o0d0dgs7klotFT" -O pubmed/raw/disease_meta.tsv && rm -rf /tmp/cookies.txt

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt


unzip "pubmed/raw/2019_merged_json_fixed.zip" -d "pubmed/raw"

rm pubmed/raw/2019_merged_json_fixed.zip

wget https://storage.googleapis.com/open-targets-data-releases/20.06/output/20.06_association_data.json.gz -O opentargets/raw
wget https://storage.googleapis.com/open-targets-data-releases/20.06/output/20.06_target_list.csv.gz -O opentargets/raw
wget https://storage.googleapis.com/open-targets-data-releases/20.06/output/20.06_disease_list.csv.gz -O opentargets/raw

gunzip opentargets/raw/20.06_association_data.json.gz -d opentargets/raw
gunzip opentargets/raw/20.06_target_list.csv.gz -d opentargets/raw
gunzip opentargets/raw/20.06_disease_list.csv.gz -d opentargets/raw

rm opentargets/raw/20.06_association_data.json.gz
rm opentargets/raw/20.06_target_list.csv.gz
rm opentargets/raw/20.06_disease_list.csv.gz

wget http://evexdb.org/pmresources/vec-space-models/PubMed-and-PMC-w2v.bin -O word2vec