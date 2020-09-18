import json
import numpy as np

with open('opentargets/processed/diseases') as fp:
    diseases_ot = fp.readlines()
    
with open('opentargets/processed/targets') as fp:
    targets_ot = fp.readlines()

with open('diseases_ot_to_bern.json') as fp:
    diseases_ot_to_bern = json.load(fp)


with open('targets_ot_to_bern.json') as fp:
    targets_ot_to_bern = json.load(fp)


i = 0

with open('pubmed/processed/diseases', 'w') as fp_d:
    for line in diseases_ot:
        _, disease = line.strip().split()
    
        if disease in diseases_ot_to_bern.keys():
            fp_d.write(f'{i}\t{diseases_ot_to_bern[disease]}\n')
            i += 1
            
    
j = 0

with open('pubmed/processed/targets', 'w') as fp_t:
    for line in targets_ot:
        _, target = line.strip().split()

        if target in targets_ot_to_bern.keys():
            fp_t.write(f'{i}\t{targets_ot_to_bern[target]}\n')
            i += 1
            j += 1
            
            
            
with open('dictionaries/pmi_dict.json') as fp:
    pmi_dict = json.load(fp)

with open('pubmed/processed/diseases') as fp:
    diseases = fp.readlines()

with open('pubmed/processed/targets') as fp:
    targets = fp.readlines()

diseases_dict = {}
targets_dict = {}

for line in diseases:
    d_id, disease = line.strip().split()
    diseases_dict[disease] = d_id

for line in targets:
    t_id, target = line.strip().split()
    targets_dict[target] = t_id

ot_dict = {**diseases_dict, **targets_dict}

i = 0

with open('pubmed/processed/relations', 'w') as fp_r:
    fp_r.write('idx\tsource\ttarget\n')
    with open('pubmed/processed/relations_names', 'w') as fp_rn:
        fp_rn.write('idx\tsource\ttarget\n')
        for e_key in pmi_dict.keys():
            for n_key in pmi_dict[e_key].keys():
                if e_key in ot_dict.keys() and n_key in ot_dict.keys() and pmi_dict[e_key][n_key] > -11.:
                    fp_r.write(f'{i}\t{ot_dict[e_key]}\t{ot_dict[n_key]}\n')
                    fp_rn.write(f'{i}\t{e_key}\t{n_key}\n')
                    i += 1
            