import json, os

occ_dict = {}

for fname in os.listdir('pubmed/raw/2019_merged_json_fixed'):
    fpath = os.path.join('pubmed/raw/2019_merged_json_fixed', fname)
    with open(fpath) as fp:
        lines = fp.readlines()
        
    for line in lines:
        data = json.loads(line)
        unique_entities = []
        entities = []
        if 'entities' in data.keys():
            for key in data['entities'].keys():
                for key_dict in data['entities'][key]:
                    if key_dict['id'] not in unique_entities:
                        unique_entities.append(key_dict['id'])
                    entities.append(key_dict['id'])

            for ent_id in unique_entities:
                occ_dict.setdefault(ent_id, {})
                for neighbor_id in entities:
                    if ent_id != neighbor_id:
                        occ_dict[ent_id][neighbor_id] = occ_dict[ent_id].setdefault(neighbor_id, 0) + 1


with open('dictionaries/occ_dict.json', 'w') as fp:
    json.dump(occ_dict, fp)
    
    
    
freq_dict = {}

for fname in os.listdir('pubmed/raw/2019_merged_json_fixed'):
    fpath = os.path.join('pubmed/raw/2019_merged_json_fixed', fname)
    with open(fpath) as fp:
        lines = fp.readlines()
        
    for line in lines:
        data = json.loads(line)
        if 'entities' in data.keys():
            for key in data['entities'].keys():
                for key_dict in data['entities'][key]:
                    ent_id = key_dict['id']
                    freq_dict[ent_id] = freq_dict.setdefault(ent_id, 0) + 1
                    
                    
pmi_dict = {}


with open('dictionaries/occ_dict.json') as fp:
    occ_dict = json.load(fp)

for ent_id in occ_dict.keys():
    pmi_dict[ent_id] = occ_dict[ent_id]
    
    for neigh_id in pmi_dict[ent_id].keys():
        pmi_dict[ent_id][neigh_id] = np.log(pmi_dict[ent_id][neigh_id] / freq_dict[ent_id] / freq_dict[neigh_id])

with open('dictionaries/pmi_dict.json', 'w') as fp:
    json.dump(pmi_dict, fp)