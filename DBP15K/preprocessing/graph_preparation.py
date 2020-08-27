import pickle, torch

# preparing ground truth dictionaries between fr and en entities
with open('processed_data/clean/ent_ILLs') as fp:
    ills = fp.readlines()

en_to_fr = {}
fr_to_en = {}

for line in ills:
    fr, en = line.strip().split()
    en_to_fr[en] = fr
    fr_to_en[fr] = en

# utility mapping from entity to node id and vice versa
en_id_to_key = {}
en_key_to_id = {}
fr_id_to_key = {}
fr_key_to_id = {}
gt = []

for i, en in enumerate(en_to_fr.keys()):
    en_id_to_key[i] = en
    en_key_to_id[en] = i
    
    fr = en_to_fr[en]
    fr_id_to_key[i] = fr
    fr_key_to_id[fr] = i
    gt.append([i, i])

# will be needed as an input to s-gwl
pickle.dump(en_id_to_key, 'processed_data/dictionaries/en_dict.pkl')
pickle.dump(fr_id_to_key, 'processed_data/dictionaries/fr_dict.pkl')

gt = torch.tensor(gt)
torch.save(gt.T, 'processed_data/graph_data/ground_truth.pt)

# utility dictionaries for relations' embeddings
with open('processed_data/aligned_embeddings/fr_relations') as fp:
    fr_rel_emb = fp.readlines()
    
fr_rel_emb_dict = {}

for line in fr_rel_emb:
    line = line.strip().split()
    rel = line[0]
    emb = line[1:]
    emb = list(map(float, emb))
    
    fr_rel_emb_dict[rel] = emb
    

with open('processed_data/aligned_embeddings/en_relations') as fp:
    en_rel_emb = fp.readlines()
    
en_rel_emb_dict = {}

for line in en_rel_emb:
    line = line.strip().split()
    rel = line[0]
    emb = line[1:]
    emb = list(map(float, emb))
    
    en_rel_emb_dict[rel] = emb

# filtering relations according to their endpoints' belonging to the mapped gt set
# and creating edge indices for both graphs
with open('processed_data/clean/fr_rel_triples') as fp:
    fr_triples = fp.readlines()


fr_edge_index = []
fr_edge_attrs = []

for triple in fr_triples:
    s, r, t = triple.strip().split()
    if s in fr_to_en.keys() and t in fr_to_en.keys():
        s_id, t_id = fr_key_to_id[s], fr_key_to_id[t]
        fr_edge_index.append([s_id, t_id])
        fr_edge_attrs.append(fr_rel_emb_dict[r])

with open('processed_data/clean/en_rel_triples') as fp:
    en_triples = fp.readlines()
        
en_edge_index = []
en_edge_attrs = []

for triple in en_triples:
    s, r, t = triple.strip().split()
    if s in en_to_fr.keys() and t in en_to_fr.keys():
        s_id, t_id = en_key_to_id[s], en_key_to_id[t]
        en_edge_index.append([s_id, t_id])
        en_edge_attrs.append(en_rel_emb_dict[r])

# saving
en_edge_index = torch.tensor(en_edge_index)
fr_edge_index = torch.tensor(fr_edge_index)
en_edge_attrs = torch.tensor(en_edge_attrs)
fr_edge_attrs = torch.tensor(fr_edge_attrs)
           
torch.save(en_edge_index.T, 'processed_data/graph_data/en_edge_index.pt')
torch.save(fr_edge_index.T, 'processed_data/graph_data/fr_edge_index.pt')
torch.save(en_edge_attrs, 'processed_data/graph_data/en_edge_attrs.pt')
torch.save(fr_edge_attrs, 'processed_data/graph_data/fr_edge_attrs.pt')


# creating the node embeddings tensors
size = (len(en_to_fr), 300) # num_nodes x emb_dim (which is predefined by fasttext)
           
with open('processed_data/aligned_embeddings/fr_entities') as fp:
    fr_ent_emb = fp.readlines()
    
fr_entities_embeddings = torch.empty(size)

for line in fr_ent_emb:
    line = line.strip().split()
    ent = line[0]
    emb = line[1:]
    emb = list(map(float, emb))
    emb = torch.tensor(emb)
    if ent in fr_to_en.keys():
        fr_id = fr_key_to_id[ent]
        fr_entities_embeddings[fr_id] = emb
        
with open('processed_data/aligned_embeddings/en_entities') as fp:
    en_ent_emb = fp.readlines()
    
en_entities_embeddings = torch.empty(size)

for line in en_ent_emb:
    line = line.strip().split()
    ent = line[0]
    emb = line[1:]
    emb = list(map(float, emb))
    emb = torch.tensor(emb)
    
    if ent in en_to_fr.keys():
        en_id = en_key_to_id[ent]
        en_entities_embeddings[en_id] = emb
        
torch.save(en_entities_embeddings, 'processed_data/graph_data/en_node_attrs.pt')
torch.save(fr_entities_embeddings, 'processed_data/graph_data/fr_node_attrs.pt')