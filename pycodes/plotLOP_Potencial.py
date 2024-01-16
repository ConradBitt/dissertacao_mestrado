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

with open('../results/data_LOP_potencial.pkl','rb') as f:
    dados_lop = pickle.load(f)

t = dados_lop['t']
t_phase = dados_lop['t_phase']
v_soma1 = dados_lop['v_soma1']
v_soma2 = dados_lop['v_soma2']
v_soma3 = dados_lop['v_soma3']
v_soma4 = dados_lop['v_soma4']
lop = dados_lop['lop']



cm = 1/2.54

fig = plt.figure(figsize=(15*cm, 9*cm))
gs = fig.add_gridspec(2, 2, height_ratios=[2, 3],width_ratios=[50,1])
fig.set_tight_layout(20)

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_title('(A)', loc='left', pad=10)
ax0.xaxis.set_visible(False)
ax0.set_ylabel('Voltage (mV)')
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.plot(t, v_soma4, color='magenta')
ax0.plot(t, v_soma1, color='red')
ax0.plot(t, v_soma2, color='green')
ax0.plot(t, v_soma3, color='blue')
ax0.set_xlim(1500, 4300)

ax1 = fig.add_subplot(gs[1,0], sharex=ax0)
n_neurons = np.arange(lop.shape[0])
tg, ig = np.meshgrid(t_phase, n_neurons)
hm2 = ax1.pcolormesh(tg, ig, lop, cmap='inferno', vmax=1.0, vmin=0.96)
ax1.set_title('(B)', loc='left', pad=10)
ax1.set_yticks([1, lop.shape[0]])
ax1.set_yticklabels(['1', '256'])
ax1.set_ylim(1, lop.shape[0] + 1)
ax1.set_xlim(2000, 4300)
ax1.set_ylabel('neurônio $n$')
ax1.set_xlabel('Tempo (ms)')

ax2 = fig.add_subplot(gs[0,1])
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.yaxis.set_visible(False)
ax2.xaxis.set_visible(False)

ax3 = fig.add_subplot(gs[1,1])
cbar2 = plt.colorbar(hm2, cax=ax3, ticks=[0.96, 1])
cbar2.set_label('LOP$(t)$')

plt.savefig('exemplo_lop_potencial.png', dpi=600, bbox_inches='tight', format='png')