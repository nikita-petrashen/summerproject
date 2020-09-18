import pandas as pd
import json

# what's happening here is the following:
# i) filtering entities from opentargets by a certain confidence score
# ii) removing entities which are not in PubMed vocabulary
# iii) creating an edge index

with open('opentargets/raw/20.06_association_data.json') as fp:
    associations = fp.readlines()

with open('dictionaries/targets_ot_to_bern.json') as fp:
    targets_ot_to_bern = json.load(fp)
    
with open('dictionaries/diseases_ot_to_bern.json') as fp:
    diseases_ot_to_bern = json.load(fp)
    
    
fp_d = open('opentargets/processed/june2020/diseases', 'w')
fp_t = open('opentargets/processed/june2020/targets', 'w')
fp_r = open('opentargets/processed/june2020/relations', 'w')
fp_rn = open('opentargets/processed/june2020/relations_names', 'w')

diseases = {}
targets = {}

i, j, k = 0, 0, 0

fp_r.write('disease target\n')

for association in associations:
    a_dict = json.loads(association)
    target = a_dict['target']['id']
    disease = a_dict['disease']['id']
    g_a = a_dict['association_score']['datatypes']['genetic_association']
    r_e = a_dict['association_score']['datatypes']['rna_expression']
    s_m = a_dict['association_score']['datatypes']['somatic_mutation']
    k_d = a_dict['association_score']['datatypes']['known_drug']
    a_m = a_dict['association_score']['datatypes']['animal_model']
    a_p = a_dict['association_score']['datatypes']['affected_pathway']
    
    if g_a == 1.0 or r_e == 1.0 or s_m == 1.0 or k_d == 1.0 or a_m == 1.0 or a_p == 1.0:
        
        if target in targets_ot_to_bern.keys() and target not in targets.keys():
            targets[target] = i
            fp_t.write(f'{i}\t{target}\n')
            i += 1

        if disease in diseases_ot_to_bern.keys() and disease not in diseases.keys():
            diseases[disease] = j
            fp_d.write(f'{j}\t{disease}\n')
            j += 1
            
        if disease in diseases_ot_to_bern.keys() and target in targets_ot_to_bern.keys():
            fp_r.write(f'{k}\t{diseases[disease]}\t{targets[target]}\n')
            fp_rn.write(f'{k}\t{disease}\t{target}\n')
            k += 1
    
fp_r.close()
fp_rn.close()
fp_t.close()
fp_d.close()                