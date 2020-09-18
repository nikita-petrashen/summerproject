import pandas as pd
import json


# to check if an entity is in Pubmed dictionary
with open('dictionaries/occ_dict.json') as fp:
    cooc_dict = json.load(fp)


# Creating dictionaries with bern-ot correspondence for diseases
disease_efo_ids = pd.read_csv('pubmed/raw/disease_efo_ids.tsv', header=0, sep='\t', low_memory=False)

# <don't ask>
diseases_bern_to_efo = {}
diseases_bern_to_orphanet = {}
diseases_bern_to_mondo = {}
diseases_bern_to_hp = {}
diseases_bern_to_doid = {}

diseases_efo_to_bern = {}
diseases_orphanet_to_bern = {}
diseases_mondo_to_bern = {}
diseases_hp_to_bern = {}
diseases_doid_to_bern = {}

for row in disease_efo_ids.dropna(subset=['external_efo_id']).iterrows():
    row = row[1]
    bern_id = row['id']
    ext_ids = row['external_efo_id'].split(',')
    for ext_id in ext_ids:
        if 'EFO' in ext_id:
            diseases_bern_to_efo.setdefault(bern_id, []).append(ext_id)
            diseases_efo_to_bern[ext_id] = bern_id
        elif 'Orphanet' in ext_id:
            diseases_bern_to_orphanet.setdefault(bern_id, []).append(ext_id)
            diseases_orphanet_to_bern[ext_id] = bern_id
        elif 'MONDO' in ext_id:
            diseases_bern_to_mondo.setdefault(bern_id, []).append(ext_id)
            diseases_mondo_to_bern[ext_id] = bern_id
        elif 'HP' in ext_id:
            diseases_bern_to_hp.setdefault(bern_id, []).append(ext_id)
            diseases_hp_to_bern[ext_id] = bern_id
        elif 'DOID' in ext_id:
            diseases_bern_to_doid.setdefault(bern_id, []).append(ext_id)
            diseases_doid_to_bern[ext_id] = bern_id
            


diseases_bern_to_ot = {**diseases_bern_to_doid, **diseases_bern_to_efo, **diseases_bern_to_hp, **diseases_bern_to_mondo, **diseases_bern_to_orphanet}

diseases_ot_to_bern = {**diseases_doid_to_bern, **diseases_efo_to_bern, **diseases_hp_to_bern, **diseases_mondo_to_bern, **diseases_orphanet_to_bern}
# <\don't ask>

with open('dictionaries/diseases_bern_to_ot.json', 'w') as fp:
    json.dump(diseases_bern_to_ot, fp)


with open('dictionaries/diseases_ot_to_bern.json', 'w') as fp:
    json.dump(diseases_ot_to_bern, fp)
    

# Creating dictionaries with bern-ot correspondence for targets
gene_meta = pd.read_csv('gene_meta.tsv', names=['BERN_ID', '1', '2', '3', 'EXT_ID', '4', '5', '6', '7', '8', '9', '10', '11'], header=None, sep='\t', low_memory=False)    # we need only 'BERN_ID' and 'EXT_ID'

targets_bern_to_ot = {}
targets_ot_to_bern = {}

for entry in gene_meta.iterrows():
    entry = entry[1]
    bern_id = entry['BERN_ID']
    if str(bern_id) in cooc_dict.keys():
        ids = entry['EXT_ID'].split('|')
        for ext_id in ids:

            ext_id = ext_id.split(':')
            if 'Ensembl' in ext_id:
                ot_id = ext_id[-1]
                targets_bern_to_ot[bern_id] = ot_id
                targets_ot_to_bern[ot_id] = bern_id
    
with open('dictionaries/targets_bern_to_ot.json', 'w') as fp:
    json.dump(targets_bern_to_ot, fp)

with open('dictionaries/targets_ot_to_bern.json', 'w') as fp:
    json.dump(targets_ot_to_bern, fp)