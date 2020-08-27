"""
    In this code I generate subsamples of DBP15K based on random walks
    and then run s-GWL on these subsamples.
"""
import sys
sys.path.append('methods')    # to import s-GWL methods (didn't work without this line in my case)

import EvaluationMeasure as Eval
import GromovWassersteinGraphToolkit as GwGt
import pickle
import time
import warnings
import numpy as np
import networkx as nx
from torch_geometric.datasets import DBP15K
import torch
from matplotlib import pyplot as plt
import os
from scipy.sparse import csr_matrix, save_npz

EPS = 1e-8
DBPROOT = ''    # change to the location of your DBP15K or suffer the downloading and preprocessing steps
RESULTSDIR = './results'    # change this to desired results folder
os.mkdir(f'{RESULTSDIR}')
os.mkdir(f'{RESULTSDIR}/smart_subsample')


def random_walk(source, adj_dict, neigh_dict, size=15):
    node_list = []
    edge_list = []
    
    cur = source
    node_list.append(cur)
    
    for i in range(size):
        nxt = np.random.choice(adj_dict[cur], p=neigh_dict[cur])
        
        while nxt > 14120:
            nxt = np.random.choice(adj_dict[cur], p=neigh_dict[cur])
            
        node_list.append(nxt)
        edge_list.append([cur, nxt])
        cur = nxt
        
    return np.unique(node_list), edge_list

def get_edges(node_list, adj_dict):
    edge_list = []

    for s in np.unique(node_list):
        for t in np.unique(node_list):
            if s in adj_dict[t] or t in adj_dict[s]:

                if [t, s] not in edge_list:
                    edge_list.append([s, t])
                    
    return edge_list

def prepare_for_sgwl(node_list, edge_list):
    n_nodes = len(node_list)
    converted_edges = []
    nodes_dict = {}
    nodes_dict_reversed = {}
    
    for i in range(n_nodes):
        nodes_dict[node_list[i]] = i
        nodes_dict_reversed[i] = node_list[i]
        
    for edge in edge_list:
        s, t = edge
        converted_edges.append([nodes_dict[s], nodes_dict[t]])
        
    adj_matrix = np.zeros((n_nodes, n_nodes))
    
    for edge in converted_edges:
        s, t = edge
        adj_matrix[s, t] = 1
        adj_matrix[t, s] = 1
        
    degree = np.sum(adj_matrix, axis=0)
    
    return nodes_dict_reversed, degree, adj_matrix


warnings.filterwarnings("ignore")

data = DBP15K(root=DBPROOT, pair='fr_en')

fr_degree_dict = {}
fr_neigh_dict = {}
fr_adj_dict = {}

for edge in data[0].edge_index1.T:
    s, t = list(map(int, edge))
    fr_degree_dict[s] = fr_degree_dict.setdefault(s, 0) + 1
    fr_degree_dict[t] = fr_degree_dict.setdefault(t, 0) + 1
    
    fr_adj_dict[s] = np.append(fr_adj_dict.setdefault(s, np.array([], dtype=int)), t)
    fr_adj_dict[t] = np.append(fr_adj_dict.setdefault(t, np.array([], dtype=int)), s)

for edge in data[0].edge_index1.T:
    s, t = list(map(int, edge))
    fr_neigh_dict[s] = np.append(fr_neigh_dict.setdefault(s, np.array([])), fr_degree_dict[t])
    fr_neigh_dict[t] = np.append(fr_neigh_dict.setdefault(t, np.array([])), fr_degree_dict[s])
    
for node in fr_neigh_dict.keys():
    fr_neigh_dict[node] = np.power(fr_neigh_dict[node], 0.7)
    fr_neigh_dict[node] /= (np.sum(fr_neigh_dict[node]) + EPS)
    
    
en_degree_dict = {}
en_neigh_dict = {}
en_adj_dict = {}

for edge in data[0].edge_index2.T:
    s, t = list(map(int, edge))
    en_degree_dict[s] = en_degree_dict.setdefault(s, 0) + 1
    en_degree_dict[t] = en_degree_dict.setdefault(t, 0) + 1
    
    en_adj_dict[s] = np.append(en_adj_dict.setdefault(s, np.array([], dtype=int)), t)
    en_adj_dict[t] = np.append(en_adj_dict.setdefault(t, np.array([], dtype=int)), s)

for edge in data[0].edge_index2.T:
    s, t = list(map(int, edge))
    en_neigh_dict[s] = np.append(en_neigh_dict.setdefault(s, np.array([])), en_degree_dict[t])
    en_neigh_dict[t] = np.append(en_neigh_dict.setdefault(t, np.array([])), en_degree_dict[s])

for node in en_neigh_dict.keys():
    en_neigh_dict[node] = np.power(en_neigh_dict[node], 0.7)
    en_neigh_dict[node] /= (np.sum(en_neigh_dict[node]) + EPS)
    
    
en_degrees = sorted(list(en_degree_dict.keys()), key=lambda x: en_degree_dict[x], reverse=True)
fr_degrees = sorted(list(fr_degree_dict.keys()), key=lambda x: fr_degree_dict[x], reverse=True)

f = open(f'{RESULTSDIR}/smart_subsample/gwl.log', 'w')
        
for walk_len in [10, 20, 50, 100, 200, 500, 1000]:
    print(f'walk_len {walk_len}')
    f.write(f'walk_len {walk_len}')
    for i in range(20):
        start_en = np.random.choice(en_degrees[:100])
        nodes_en, edges_en = random_walk(start_en, en_adj_dict, en_neigh_dict, size=walk_len)
        nodes_fr, edges_fr = nodes_en, get_edges(nodes_en, fr_adj_dict)
        
        en_dict, en_deg, en_adj = prepare_for_sgwl(nodes_en, edges_en)
        fr_dict, fr_deg, fr_adj = prepare_for_sgwl(nodes_fr, edges_fr)
        
        
        num_iter = 2000
        ot_dict = {'loss_type': 'L2',  # the key hyperparameters of GW distance
                   'ot_method': 'proximal',
                   'beta': 0.025,
                   'outer_iteration': num_iter,
                   # outer, inner iteration, error bound of optimal transport
                   'iter_bound': 1e-30,
                   'inner_iteration': 2,
                   'sk_bound': 1e-30,
                   'node_prior': 1e3,
                   'max_iter': 4,  # iteration and error bound for calcuating barycenter
                   'cost_bound': 1e-26,
                   'update_p': False,  # optional updates of source distribution
                   'lr': 0,
                   'alpha': 0}


        cost_s = fr_adj
        cost_t = en_adj

        p_s = fr_deg
        p_t = en_deg

        p_s = p_s.reshape((-1, 1))
        p_t = p_t.reshape((-1, 1))

        idx2node_s = fr_dict
        idx2node_t = en_dict

        num_nodes = cost_s.shape[0]

        time_s = time.time()
        ot_dict['outer_iteration'] = num_iter
        pairs_idx, pairs_name, pairs_confidence = GwGt.direct_graph_matching(
            0.5 * (cost_s + cost_s.T), 0.5 * (cost_t + cost_t.T), p_s, p_t, idx2node_s, idx2node_t, ot_dict)
        runtime = time.time() - time_s
        nc = Eval.calculate_node_correctness(pairs_name, num_correspondence=num_nodes)
        

        if walk_len in [10, 20]:
            g_en = nx.Graph()
            g_en.add_nodes_from(nodes_en)
            g_en.add_edges_from(edges_en)
            g_fr = nx.Graph()
            g_fr.add_nodes_from(nodes_fr)
            g_fr.add_edges_from(edges_fr)
            
            pair_idx = np.array(pairs_idx).T
            if_correct = (pair_idx[0] == pair_idx[1]).astype(int)
            plt.figure(figsize=(20, 13))
            plt.subplot(1, 2, 1)
            nx.draw(g_en, node_color=if_correct)
            plt.title('en')
            plt.subplot(1, 2, 2)
            
            nx.draw(g_fr, node_color=if_correct)
            plt.title('fr')
            plt.suptitle(f'acc = {nc}')
            plt.savefig(f'{RESULTSDIR}/smart_subsample/{walk_len}.{i}.jpg')
            
        print(f'\t{i} acc: {nc:.4f}, runtime: {runtime/60:.2f}') 
        f.write(f'\t{i} acc: {nc:.4f}, runtime: {runtime/60:.2f}')
        
f.close()






