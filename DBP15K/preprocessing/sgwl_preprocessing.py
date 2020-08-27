import numpy as np
from scipy.sparse import csr_matrix, save_npz
import os
import pickle

# due to high working time of this algorithm I decided to test it
# on small subsamples of DBP15K graph. subsamples were generated
# as subgraphs on $size vertices with the highest degrees


# creating directories
os.mkdir('processed_data/sgwl_data')
# subgraph on a set of nodes of size $size
for size in [100, 300, 500, 1000, 2000, 4000, 15000]:
    os.mkdir(f'processed_data/sgwl_data/{size}')

# for sgwl we will need three objects for each graph: degree sequence of its nodes,
# adjacency matrix in sparse csr format and a dictionary of nodes' names (not really of any utility)
with open('processed_data/dictionaries/en_dict.pkl') as fp:
    en_dict = pickle.load(fp)
with open('processed_data/dictionaries/fr_dict.pkl') as fp:
    fr_dict = pickle.load(fp)

with open('processed_data/clean/en_rel_triples') as fp:
    fp.readline()
    lines = fp.readlines()

en_degrees = np.zeros(15000)
en_adj = np.empty((2, len(lines)))
en_values = np.ones(len(lines))

for i, line in enumerate(lines):
    source, target, _ = line.strip().split()
    source, target = map(int, [source, target])
    en_degrees[source] += 1
    en_degrees[target] += 1
    en_adj[0, i] = source
    en_adj[1, i] = target

print(f'en num edges: {len(lines)}')
    
with open('processed_data/clean/fr_rel_triples') as fp:
    fp.readline()
    lines = fp.readlines()

fr_degrees = np.zeros(15000)
fr_adj = np.empty((2, len(lines)))
fr_values = np.ones(len(lines))

for i, line in enumerate(lines):
    source, target, _ = line.strip().split()
    source, target = map(int, [source, target])
    fr_degrees[source] += 1
    fr_degrees[target] += 1
    fr_adj[0, i] = source
    fr_adj[1, i] = target

print(f'fr num edges: {len(lines)}')

en_nodes_sorted = np.argsort(en_degrees)[::-1]
en_num_edges = 101082
fr_num_edges = 93020

# generating subsamples
for size in [100, 300, 500, 1000, 2000, 4000, 15000]:
    
    en_dict_subset = {i: en_dict[str(key)] for i, key in enumerate(en_nodes_sorted[ :size])}
    fr_dict_subset = {i: fr_dict[str(key)] for i, key in enumerate(en_nodes_sorted[ :size])}
    pickle.dump(en_dict_subset, open(f'processed_data/sgwl_data/{size}/en_dict.pkl', 'wb'))
    pickle.dump(fr_dict_subset, open(f'processed_data/sgwl_data/{size}/fr_dict.pkl', 'wb'))
    
    en_degrees_subset = [en_degrees[i] for i in en_nodes_sorted[ :size]]
    fr_degrees_subset = [fr_degrees[i] for i in en_nodes_sorted[ :size]]
    
    en_adj_subset, fr_adj_subset = [], []
    
    for i in range(en_num_edges):
        s, t = en_adj[0, i], en_adj[1, i]
        if s in en_nodes_sorted[ :size] and t in en_nodes_sorted[ :size]:
            s_new = np.where(en_nodes_sorted[ :size]==s)[0][0]
            t_new = np.where(en_nodes_sorted[ :size]==t)[0][0]
            en_adj_subset.append([s_new, t_new])
    
    for i in range(fr_num_edges):
        s, t = fr_adj[0, i], fr_adj[1, i]
        if s in en_nodes_sorted[ :size] and t in en_nodes_sorted[ :size]:
            s_new = np.where(en_nodes_sorted[ :size]==s)[0][0]
            t_new = np.where(en_nodes_sorted[ :size]==t)[0][0]
            fr_adj_subset.append([s_new, t_new])
            
    print(f'size: {size}, num_en_edges: {len(en_adj_subset)}, num_fr_edges: {len(fr_adj_subset)}')
    en_degrees_subset = np.array(en_degrees_subset) / sum(en_degrees_subset)
    fr_degrees_subset = np.array(fr_degrees_subset) / sum(fr_degrees_subset)
    np.save(f'processed_data/sgwl_data/{size}/fr_deg.npy', np.array(fr_degrees_subset))
    np.save(f'processed_data/sgwl_data/{size}/en_deg.npy', np.array(en_degrees_subset))
    
    en_adj_subset = np.array(en_adj_subset).T
    fr_adj_subset = np.array(fr_adj_subset).T
    
    en_values_subset = np.ones(en_adj_subset.shape[1])
    fr_values_subset = np.ones(fr_adj_subset.shape[1])
    en_adj_matrix_subset = csr_matrix((en_values_subset, en_adj_subset), shape=(size, size))
    fr_adj_matrix_subset = csr_matrix((fr_values_subset, fr_adj_subset), shape=(size, size))
    
    save_npz(f'processed_data/sgwl_data/{size}/fr_adj.npz', fr_adj_matrix_subset)
    save_npz(f'processed_data/sgwl_data/{size}/en_adj.npz', en_adj_matrix_subset)