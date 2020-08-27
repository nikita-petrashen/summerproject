"""
Data preparation for PPI dataset

database = {'costs': a list of adjacency matrices of different graphs,
            'probs': a list of distributions of nodes in different graphs,
            'idx2nodes': a list of dictionaries mapping index to node name,
            'correspondence': None or a list of correspondence set}
"""
import sys
sys.path.append('methods')

import EvaluationMeasure as Eval
import GromovWassersteinGraphToolkit as GwGt
import pickle
import time
import warnings
from scipy.sparse import load_npz
import pickle
import argparse
import numpy as np
import os

# change these accordingly
DATAPATH = 'processed_data/sgwl_data'
RESULTSDIR = '.'

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=int, required=True)

args = parser.parse_args()

size = args.size

warnings.filterwarnings("ignore")

database = {}
fr_adj = load_npz(f'{DATAPATH}/{size}/fr_adj.npz')
en_adj = load_npz(f'{DATAPATH}/{size}/en_adj.npz')

fr_deg = np.load(f'{DATAPATH}/{size}/fr_deg.npy')
en_deg = np.load(f'{DATAPATH}/{size}/en_deg.npy')

with open(f'{DATAPATH}/{size}/en_dict.pkl', 'rb') as fp:
    en_dict = pickle.load(fp)
    
with open(f'{DATAPATH}/{size}/fr_dict.pkl', 'rb') as fp:
    fr_dict = pickle.load(fp)



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

num_nodes = size

time_s = time.time()
ot_dict['outer_iteration'] = num_iter
pairs_idx, pairs_name, pairs_confidence = GwGt.direct_graph_matching(
    0.5 * (cost_s + cost_s.T), 0.5 * (cost_t + cost_t.T), p_s, p_t, idx2node_s, idx2node_t, ot_dict)
runtime = time.time() - time_s
nc = Eval.calculate_node_correctness(pairs_name, num_correspondence=num_nodes)
print('method: gwl, duration {:.4f}s, nc {:.4f}.'.format(runtime, nc))

with open(f'{RESULTSDIR}/{size}/gwl_{size}.log', 'w') as f:
    f.write(f'acc: {nc:.4f}, runtime: {runtime/60:.2f}')
    
time_s = time.time()
ot_dict['outer_iteration'] = num_iter
pairs_idx, pairs_name, pairs_confidence = GwGt.recursive_direct_graph_matching(
    0.5 * (cost_s + cost_s.T), 0.5 * (cost_t + cost_t.T), p_s, p_t, idx2node_s, idx2node_t, ot_dict,
    weights=None, predefine_barycenter=False, cluster_num=2,
    partition_level=3, max_node_num=0)
runtime = time.time() - time_s
nc = Eval.calculate_node_correctness(pairs_name, num_correspondence=num_nodes)
print('method: s-gwl, duration {:.4f}s, nc {:.4f}.'.format(runtime, nc))

with open(f'{RESULTSDIR}/{size}/sgwl_{size}.log', 'w') as f:
    f.write(f'acc: {nc:.4f}, runtime: {runtime/60:.2f}')




