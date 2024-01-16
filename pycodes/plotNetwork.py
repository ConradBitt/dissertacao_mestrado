import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
import sys

def get_matriz_Adjacência(n, p, numExtraConex = 0):
    conex = np.zeros((n, n))  # acoplamento não-local
    for i in range(n):
        for k in range(i - p, i + p + 1):
            j = k % n  # Utilize o operador de módulo para garantir que j permaneça dentro do intervalo correto
            if i != j:
                conex[i, j] = 1  # Defina 1 para representar a existência de uma aresta

    # Introduzir conexões aleatórias
    conex_smll = np.zeros_like(conex)
    conex_smll += conex

    for linha, conexoes in enumerate(conex_smll):
        for conexExtra in range(numExtraConex):
            idx_nova_conex = np.random.randint(0, n)  # gera índice aleatório de 0 a n
            if idx_nova_conex == 0 or idx_nova_conex == n:
                idx_nova_conex = idx_nova_conex % n

            if conexoes[idx_nova_conex] != 1:
                conexoes[idx_nova_conex] = 1

    # Remover autoconexões
    for i in range(n):
        conex_smll[i, i] = 0

    return conex_smll



def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['font.family'] = 'STIXGeneral'

plot_params()

# v = str(sys.argv[1])
# i = str(sys.argv[2])
# j = str(sys.argv[3])
# folder = f'figuresV2'
file = f'exemplo_rede'

# print('~~ Plot Raster, LOP, Phase and GOP.')
# print(f'Reading: "{file}"')

# with open(file+'_data.pkl', 'rb') as f:
#     data = pickle.load(f)

# cellNumber = data['simConfig']['cellNumber']
# gex = data['simConfig']['gex']
# amp = data['simConfig']['IClamp0']['amp'] * 1000
# neighbours = data['simConfig']['n_neighbors']
# freq_mean = data['freq_bar'].mean()
# coresPerNode = data['simConfig']['coresPerNode']


np.random.seed(457892137)

######## Teste:
cell_number = 20
r = 50  # radius
center = (50, 50) # center in um
theta = np.linspace(0, 2*np.pi, cell_number)  # angle 
x = center[0] + r*np.cos(theta) # x-values in um
z = center[1] + r*np.sin(theta) # z-values in um

nao_local = get_matriz_Adjacência(cell_number, 2, 0)
aleatoria = get_matriz_Adjacência(cell_number, 0, int(0.05*cell_number))
small_world = get_matriz_Adjacência(cell_number, 5, int(0.1*cell_number))

# x = np.zeros(cellNumber)
# z = np.zeros(cellNumber)

# for i, cell in enumerate(data['net']['cells']):
#     x[i] = cell['tags']['x']
#     z[i] = cell['tags']['z']

cm = 1/2.54  # centimeters in inches

# f, ax = plt.subplots(figsize=(12*cm, 12*cm))
fig, ax = plt.subplots(ncols=3, figsize=(20*cm, 6*cm))


# Traçar linhas com base na matriz de adjacência

def cria_sinapses(x, z, matrix, axis):
    for i in range(len(x)):
        for j in range(len(x)):
            if matrix[i, j] != 0:
                axis.plot([x[i], x[j]], [z[i], z[j]], linestyle='-', color='blue', alpha=0.2)
    axis.plot([x[0], x[1]], [z[0], z[1]], linestyle='-', color='blue', alpha=0.4)
    axis.scatter(x,z, s=5, color='black')

cria_sinapses(x,z, nao_local, ax[0])
cria_sinapses(x,z, aleatoria, ax[1])
cria_sinapses(x,z, small_world, ax[2])

ax[0].scatter(x,z, s=5, color='black', label='Neurônios')
ax[0].plot([x[0], x[1]], [z[0], z[1]], linestyle='-', color='blue', alpha=0.4, label='Sinapses')
ax[0].legend(loc='center')
# ax[0].legend(bbox_to_anchor=(0.5, 0.5))

letter = ['(A)', '(B)','(C)']

for i, axis in enumerate(ax):
    axis.set_title(letter[i], pad=20, loc='left')
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.set_xlabel('$X$  $(\mu m)$')
ax[0].set_ylabel('$Z$  $(\mu m)$')

# ax.set_xlim(40,60)
# ax.set_ylim(0,20)

plt.savefig(file+'_rede.png', dpi=600, bbox_inches='tight', format='png')
