import pickle
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

from matplotlib.colors import ListedColormap,LinearSegmentedColormap
colors = ["darkorange", "gold", "lawngreen", "lightseagreen","darkgreen"]
cmap_LOP = ListedColormap(colors)

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


def plot_LOP(t_sample, lop, vizinhos):
    cm = 1/2.54
    fig, ax2 = plt.subplots(ncols=1, nrows=1, figsize=(12*cm,5*cm))
    fig.set_tight_layout(20)
    n_neurons = np.arange(lop.shape[0])
    tg, ig = np.meshgrid(t_sample/1000, n_neurons)
    hm2 = ax2.pcolor(tg, ig, lop, cmap='inferno', vmax=1.0, vmin=0.95)#cmap_LOP)

    ax2.set_yticks([1,lop.shape[0]])
    ax2.set_yticklabels(['1','256'])
    ax2.set_ylim(1,lop.shape[0]+1)
    # ax2.set_xlim(15,19)
    cbar2= plt.colorbar(hm2, ax=ax2, ticks=[.95, 1])
    cbar2.set_label('LOP$(t)$',fontsize=9)
    ax2.set_ylabel('$n$ neurônio')
    ax2.set_xlabel('Tempo (s)')
    plt.savefig(file+f'_PlotLOP.png', dpi=600, bbox_inches='tight')

v = str(sys.argv[1])
i = str(sys.argv[2])
j = str(sys.argv[3])
folder = f'../figuresV2/'
file = f'v{v}_batch1_{i}_{j}'

# file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
# file = f'../data/v0_batch0/v0_batch0'
print('~~ Plot Raster, LOP, Phase and GOP.')
print(f'Reading: "{folder+file}"')

with open(folder+file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber

lops = data['LOP_delta']
t_phase = data['t_phase']


for delta, lop in lops.items():
    print(f'--> Plot LOP: delta = {delta}')
    plot_LOP(t_phase, lop, vizinhos=delta)

print('\n~~')



