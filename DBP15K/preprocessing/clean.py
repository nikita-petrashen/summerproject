import os

DATA_PATH = 'raw_data'
CLEAN_PATH = 'processed_data/clean'


# converting entity and relation descriptions from source files
# from URLs to entity and relation names


with open(os.path.join(DATA_PATH, 'fr_rel_triples'), 'r') as fp:
    s_triples = fp.readlines()
    
with open(os.path.join(CLEAN_PATH, 'fr_rel_triples'), 'w') as fp:
    for line in s_triples:
        triple = line.strip().split('\t')
        for entry in triple:
            fp.write(entry.split('/')[-1])
            fp.write('\t')
        fp.write('\n')
        
with open(os.path.join(DATA_PATH, 'en_rel_triples'), 'r') as fp:
    t_triples = fp.readlines()
    
with open(os.path.join(CLEAN_PATH, 'en_rel_triples'), 'w') as fp:
    for line in t_triples:
        triple = line.strip().split('\t')
        for entry in triple:
            fp.write(entry.split('/')[-1])
            fp.write('\t')
        fp.write('\n')
        
with open(os.path.join(DATA_PATH, 'ent_ILLs'), 'r') as fp:
    ills = fp.readlines()

with open(os.path.join(CLEAN_PATH, 'ent_ILLs'), 'w') as fp:
    for line in ills:
        triple = line.strip().split('\t')
        for entry in triple:
            fp.write(entry.split('/')[-1])
            fp.write('\t')
        fp.write('\n')
          
            
# forming files with entities' and relations' names to produce embeddings

with open(os.path.join(CLEAN_PATH, 'fr_rel_triples')) as fp:
    s_triples = fp.readlines()
    
entities = []
relations = []
with open(os.path.join(CLEAN_PATH, 'fr_entities'), 'w') as fp_entities:
    with open(os.path.join(CLEAN_PATH, 'fr_relations'), 'w') as fp_relations:
        for line in s_triples:
            triple = line.strip().split('\t')
            s_entity = triple[0]
            rel = triple[1]
            t_entity = triple[2]
            
            if s_entity not in entities:
                entities.append(s_entity)
                fp_entities.write(s_entity)
                fp_entities.write('\n')
                
            if t_entity not in entities:
                entities.append(t_entity)
                fp_entities.write(t_entity)
                fp_entities.write('\n')
                
            if rel not in relations:
                relations.append(rel)
                fp_relations.write(rel)
                fp_relations.write('\n')
                
                
with open(os.path.join(CLEAN_PATH, 'en_rel_triples')) as fp:
    t_triples = fp.readlines()

entities = []
relations = []
with open(os.path.join(CLEAN_PATH, 'en_entities'), 'w') as fp_entities:
    with open(os.path.join(CLEAN_PATH, 'en_relations'), 'w') as fp_relations:
        for line in t_triples:
            triple = line.strip().split('\t')
            s_entity = triple[0]
            rel = triple[1]
            t_entity = triple[2]
            
            if s_entity not in entities:
                entities.append(s_entity)
                fp_entities.write(s_entity)
                fp_entities.write('\n')
                
            if t_entity not in entities:
                entities.append(t_entity)
                fp_entities.write(t_entity)
                fp_entities.write('\n')
                
            if rel not in relations:
                relations.append(rel)
                fp_relations.write(rel)
                fp_relations.write('\n')