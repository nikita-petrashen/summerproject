from gensim.models import KeyedVectors
import json
import torch
import pandas as pd, numpy as np



pubmed_wv = KeyedVectors.load_word2vec_format('word2vec/PubMed-and-PMC-w2v.bin', binary=True)


with open('opentargets/processed/targets') as fp:
    targets = fp.readlines()

with open('opentargets/processed/diseases') as fp:
    diseases = fp.readlines()

    
    
diseases_df = pd.read_csv('opentargets/raw/20.06_disease_list.csv', header=0)
targets_df = pd.read_csv('opentargets/raw/20.06_target_list.csv', header=0)

diseases_desc = {}
targets_desc = {}

for row in diseases_df.iterrows():
    row = row[1]
    efo_id, name = row['efo_id'], row['disease_full_name']
    
    diseases_desc[efo_id] = name

for row in targets_df.iterrows():
    row = row[1]
    ensembl_id, name = row['ensembl_id'], row['hgnc_approved_symbol']
    
    targets_desc[ensembl_id] = name
    
    
    
    
emb_list = []
i, j = 0, 0
no_desc = 0
no_wv = 0

for line in diseases:
    node_id, ot_id = line.strip().split()
    if ot_id in diseases_desc.keys():
        desc = diseases_desc[ot_id]
        desc_valid = [word for word in desc.replace('-', ' ').split() if word in pubmed_wv]
        
        if desc_valid:
            emb = np.zeros(200)
            for word in desc_valid:
                emb += pubmed_wv[word]    
        else:
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            i += 1
            no_wv += 1
    else:
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            i += 1
            no_desc += 1
            
    emb_list.append(emb)
    
    
    
for line in targets:
    node_id, ot_id = line.strip().split()
    if ot_id in targets_desc.keys():
        desc = targets_desc[ot_id]
    
        if desc in pubmed_wv:
            emb = pubmed_wv[desc]
        else:
            no_wv += 1
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            j += 1
    else:
            no_desc += 1
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            j += 1
            
    emb_list.append(emb)
    
    
emb_tensor = torch.tensor(emb_list)
torch.save(emb_tensor, 'graph_data/ot_node_embeddings.pt')


with open('opentargets/processed/relations') as fp:
    fp.readline()
    relations = fp.readlines()
    
    
    
edge_index = []
edge_embeddings = []

for line in relations:
    _, s_id, t_id = list(map(int, line.strip().split()))
    edge_index.append([s_id, t_id])
    edge_embeddings.append(emb_tensor[s_id] - emb_tensor[t_id])
    edge_index.append([t_id, s_id])
    edge_embeddings.append(emb_tensor[t_id] - emb_tensor[s_id])

edge_index = torch.tensor(np.array(edge_index).T)
edge_embeddings = torch.stack(edge_embeddings)

torch.save(edge_index, 'graph_data/ot_edge_index.pt')
torch.save(edge_embeddings, 'graph_data/ot_edge_embeddings.pt')