from gensim.models import KeyedVectors
import json
import torch
import pandas as pd, numpy as np



pubmed_wv = KeyedVectors.load_word2vec_format('word2vec/PubMed-and-PMC-w2v.bin', binary=True)


with open('pubmed/processed/targets') as fp:
    targets = fp.readlines()

with open('pubmed/processed/diseases') as fp:
    diseases = fp.readlines()

with open('diseases_bern_to_ot.json') as fp:
    diseases_dict = json.load(fp)


with open('targets_bern_to_ot.json') as fp:
    targets_dict = json.load(fp)

    
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

for line in diseases:
    node_id, bern_id = line.strip().split()
    ot_id_list = diseases_dict[bern_id]
    desc = [diseases_desc[ot_id] for ot_id in ot_id_list if ot_id in diseases_desc.keys()]
    if desc:
        desc = ' '.join(desc).lower()
        emb = np.zeros(200)
        desc_valid = [word for word in desc.split() if word in pubmed_wv]
        
        if desc_valid:
            for word in desc_valid:
                if word in pubmed_wv:
                    emb += pubmed_wv[word]
        else:
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            i += 1
        
    else:
        emb = np.random.randn(200)
        emb /= np.linalg.norm(emb)
        i += 1
    
    emb_list.append(emb)
    
    
for line in targets:
    node_id, bern_id = line.strip().split()
    ot_id = targets_dict[bern_id]
    if ot_id in targets_desc.keys():
        desc = targets_desc[ot_id]
    
        if desc in pubmed_wv:
            emb = pubmed_wv[desc]
        else:
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            j += 1
    else:
            emb = np.random.randn(200)
            emb /= np.linalg.norm(emb)
            j += 1
            
    emb_list.append(emb)
    
emb_tensor = torch.tensor(emb_list)
torch.save(emb_tensor, 'graph_data/pm_node_embeddings.pt')



with open('pubmed/processed/relations') as fp:
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

edge_index = torch.tensor(edge_index).T
edge_embeddings = torch.stack(edge_embeddings)

torch.save(edge_index, 'graph_data/pm_edge_index.pt')
torch.save(edge_embeddings, 'graph_data/pm_edge_embeddings.pt')



with open('opentargets/processed/diseases') as fp:
    diseases_ot = fp.readlines()

with open('opentargets/processed/targets') as fp:
    targets_ot = fp.readlines()

ot_ids_dict = {}

for line in diseases_ot:
    t_id, ot_id = line.strip().split()
    ot_ids_dict[ot_id] = t_id

for line in targets_ot:
    t_id, ot_id = line.strip().split()
    ot_ids_dict[ot_id] = t_id
    
gt = []

for line in diseases:
    s_id, bern_id = line.strip().split()
    ot_ids = diseases_dict[bern_id]
    for ot_id in ot_ids:
        if ot_id in ot_ids_dict.keys():
            t_id = ot_ids_dict[ot_id]
            gt.append([s_id, t_id])

for line in targets:
    s_id, bern_id = line.strip().split()
    ot_id = targets_dict[bern_id]
    if ot_id in ot_ids_dict.keys():
        t_id = ot_ids_dict[ot_id]
        gt.append([s_id, t_id])
        
gt = torch.tensor(gt).T
torch.save(gt, 'graph_data/gt.pt')
