import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import locale
import latex
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

cores = list(mcolors.TABLEAU_COLORS.keys())
cores = [cor.split(':')[-1] for cor in cores]

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()


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

rede = 51
p = 5

nao_local = get_matriz_Adjacência(rede, p, 0)
aleatoria = get_matriz_Adjacência(rede, 0, int(0.25*rede))
small_world = get_matriz_Adjacência(rede, 5, int(0.25*rede))

cm = 1/2.54

fig, ax = plt.subplots(ncols=3, figsize=(20*cm, 8*cm))
fig.set_tight_layout(20)

ax[0].set_title('(A)', pad=20, loc='left')
ax[0].matshow(nao_local, cmap='binary')

ax[1].set_title('(B)', pad=20, loc='left')
ax[1].matshow(aleatoria, cmap='binary')

ax[2].set_title('(C)', pad=20, loc='left')
ax[2].matshow(small_world, cmap='binary')

for axis in ax:
    axis.xaxis.tick_bottom()
    axis.set_xlabel('$j$')
ax[0].set_ylabel('$n$', rotation=0, labelpad=20)

plt.savefig('matrizAdjacencia.png',  dpi=600, bbox_inches='tight', format='png')