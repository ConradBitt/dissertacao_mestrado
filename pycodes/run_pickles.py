"""
run_batches.py

Python script to run n-th batches.

    - When executing a parameter space grid in parallel, computational limitations often prevent gridding 100x100 in a single simulation.
      Therefore, we separate them into batches, create lists with the parameters (in this case, gex and n_cons_network), and apply the array_split function
      to partition the list into equal parts to pass to the batch.py file. This allows running numerous batches to traverse a grid of parameter spaces.

    - In batchs.infos you can read about python commands executed in run_batches.py
    - In preprocessing.err you can read about errors in preprocessing.py
    - In readpickle.err you can read about errors in readpickle.py


Parameters: 
    - python3 batch.py version batch_number param1

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np
import time 
import pickle

try:
    from __main__ import cfg  # Import the SimConfig object with parameters from the parent module
except:
    from cfg import cfg

# Information about the resolution of the parameter space
n = cfg.cellNumber
resol = 32
gex = [round(1e-5*vv, 6) for vv in np.linspace(10, 45, resol)]
p = np.linspace((resol/(8*n)), 0.40, resol)
n_cons_network = np.array([x+1 if x % 2 != 0 else x for x in (n * p).astype(int)], dtype=int)
ncons = np.array_split(n_cons_network, 4)
amps = np.round(np.linspace(0.14, 0.25, 32),4)
coresPerNode = [2, 4, 8]


batch = 1
v = 1
delta_max = 5


# arrays to space param
n_batchs = 32
n_subbatchs = 32
space_param = {
    'gex': np.zeros(n_batchs * n_subbatchs),
    'amp': np.zeros(n_batchs * n_subbatchs),
    'neighbours': np.zeros(n_batchs * n_subbatchs),
    'mean_GOP': np.zeros(n_batchs * n_subbatchs),
    'mean_LOP': np.zeros(n_batchs * n_subbatchs),
    'mean_freq': np.zeros(n_batchs * n_subbatchs),
    'mean_cv': np.zeros(n_batchs * n_subbatchs),
}

# # Cria dicionário 
with open(f'../data/space_param_v{v}_batch1.pkl', 'wb') as handle:
    pickle.dump(space_param, handle, protocol=pickle.HIGHEST_PROTOCOL)


command = 'ipython batch.py {v} {batch} {neuronPerCore}'
with open('../data/batchs.infos', 'a') as infos:
    infos.writelines(command+'\n')

# i = 0
# for cpn in coresPerNode:
#     command = f'ipython batch.py {v} {batch} {cpn}'
#     with open('../data/batchs.infos', 'a') as infos:
#         infos.writelines(command+'\n')
#     os.system(command)
    
#     print(20*'=--=')
#     print(10*' ' + f' Running {batch}')
#     print(20*'=--=')
#     batch+=1

# batch = 1
# for cpn in coresPerNode:
#     os.system(f'python3 preprocessing.py {v} {batch} 0 {delta_max}')
#     batch += 1
    
indice = 0
batch = 0
for i in range(32):
    # readfiles
    for j in range(32):
        # readpickle to create space param .pkl
        os.system(f'python3 readpickle.py {v} {i} {j} {indice}')
        indice+=1