import sys
import pickle
import numpy as np
import os

# Captura argumentos da linha de comando
v = str(sys.argv[1])
i = int(sys.argv[2])
j = int(sys.argv[3])
indice = int(sys.argv[4])

file = f'../data/v{v}_batch1/v{v}_batch1_{i}_{j}'

# Abre o arquivo e carrega os resultados usando pickle
try:
    with open(file + '_data.pkl', 'rb') as f:
        # Exibe mensagem indicando o arquivo que está sendo lido
        print(f'~ Read file: {file}_data.pkl')
        arq_resultados = pickle.load(f)
except Exception as e:
    with open('../data/readpickle.err', 'a') as f:
        f.writelines(f'Errors: {e}\n')
    sys.exit()

try:
    # Extrai variáveis específicas dos resultados
    gex = arq_resultados['simConfig']['gex']
    amp = arq_resultados['simConfig']['IClamp0']['amp']
    neighbours = arq_resultados['simConfig']['n_neighbors']
    mean_GOP = arq_resultados['GOP'].mean()
    mean_LOP = arq_resultados['LOP_delta'][5].mean(axis=1).mean()
    mean_freq = np.mean(arq_resultados['freq_bar'])
    mean_cv = np.mean(arq_resultados['cv'])
    cv_lop = arq_resultados['cv_LOP_delta']
except KeyError as e:
    with open('../data/readpickle.key_err', 'a') as f:
        f.writelines(f'Errors: {file} | Error: {e} \n')
    os.system(f'python3 preprocessing.py {v} {i} {j}')
    
    try:
        with open(file + '_data.pkl', 'rb') as f:
            # Exibe mensagem indicando o arquivo que está sendo lido
            print(f'~ Read file: {file}_data.pkl')
            arq_resultados = pickle.load(f)
    except Exception as e:
        with open('../data/readpickle.err', 'a') as f:
            f.writelines(f'Errors: {e}\n')

    gex = arq_resultados['simConfig']['gex']
    amp = arq_resultados['simConfig']['IClamp0']['amp']
    neighbours = arq_resultados['simConfig']['n_neighbors']
    mean_GOP = arq_resultados['GOP'].mean()
    mean_LOP = arq_resultados['LOP_delta'][5].mean(axis=1).mean()
    mean_freq = np.mean(arq_resultados['freq_bar'])
    mean_cv = np.mean(arq_resultados['cv'])
    cv_lop = arq_resultados['cv_LOP_delta']


# Tenta abrir o arquivo de espaço de parâmetros, cria um novo se não existir
try:
    with open(f'../data/v{v}_batch1/space_param_v{v}_batch1.pkl', 'rb') as f:  # Modificado 'wb' para 'rb'
        space_param = pickle.load(f)
except Exception as e:
    with open('../data/readpickle_space_param.err', 'a') as log:
        log.writelines(f'Errors: {e}\n')
    sys.exit()

# Adiciona os dados extraídos ao dicionário space_param

space_param['gex'][indice] = gex
space_param['amp'][indice] = amp
space_param['neighbours'][indice] = neighbours
space_param['mean_GOP'][indice] = mean_GOP
space_param['mean_LOP'][indice] = mean_LOP
space_param['mean_freq'][indice] = mean_freq
space_param['mean_cv'][indice] = mean_cv
space_param['cv_lop'][indice] = cv_lop


# Exibe mensagem indicando que o arquivo pickle está sendo salvo
print(f'~ Dump pickle file: ../data/space_param_V{v}.pkl')

# Salva o dicionário atualizado em um arquivo pickle
with open(f'../data/v{v}_batch1/space_param_v{v}_batch1.pkl', 'wb') as handle:
    pickle.dump(space_param, handle, protocol=pickle.HIGHEST_PROTOCOL)

del arq_resultados
del space_param
print('\n')
