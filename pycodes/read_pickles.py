import os
import numpy as np
import pickle

readpickles = """#!/bin/bash
#SBATCH --nodes=1                    # para rodar 1024 jobs e fazer 32x32
#SBATCH --ntasks-per-node=128        # tasks per node
#SBATCH --time=2:00:00              # time limits: 4 hour
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end


"""

resolution_space_param = 32 # 32 x 32

v = 1

# arrays to space param
space_param = {
    'gex': np.zeros(resolution_space_param * resolution_space_param),
    'amp': np.zeros(resolution_space_param * resolution_space_param),
    'neighbours': np.zeros(resolution_space_param * resolution_space_param),
    'mean_GOP': np.zeros(resolution_space_param * resolution_space_param),
    'mean_LOP': np.zeros(resolution_space_param * resolution_space_param),
    'mean_freq': np.zeros(resolution_space_param * resolution_space_param),
    'mean_cv': np.zeros(resolution_space_param * resolution_space_param),
    'cv_lop':np.zeros(resolution_space_param * resolution_space_param),
}

# # Cria dicionário 
with open(f'../data/v{v}_batch1/space_param_v{v}_batch1.pkl', 'wb') as handle:
    pickle.dump(space_param, handle, protocol=pickle.HIGHEST_PROTOCOL)

readpickle = lambda v, i, j, indice : f'python readpickle.py {v} {i} {j} {indice}'
# readpickle = lambda v, i, j, indice : f'mpiexec -n 1 python readpickle.py {v} {i} {j} {indice}'

indice = 0
for i in range(0, resolution_space_param):
    for j in range(0, resolution_space_param):
        # readpickles += readpickle(2, i, j, indice) + ' &\n'
        os.system(readpickle(1, i, j, indice))
        indice+=1

# with open('readpickles.sh', 'w+') as rodar_sh:
#     rodar_sh.writelines(readpickles)

# os.system('sbatch readpickles.sh')



