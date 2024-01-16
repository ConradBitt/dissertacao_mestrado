import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
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
    plt.rcParams["axes.formatter.limits"] = (-0.5, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()


gm = 3.5e-5
iext = 170/100
tf = 100
dur = 80
delay = 10
yamada = 'Yamada'
hh = 'hh'

os.system(f'python3 createCell.py {gm} {tf} {iext} {dur} {delay} {yamada}')

os.system(f'python3 createCell.py {0} {tf} {iext} {dur} {delay} {hh}')

with open(f'cell{yamada}.pkl','rb') as cellFile:
    yamada_data = pickle.load(cellFile)
    
with open(f'cell{hh}.pkl','rb') as cellFile:
    hh_data = pickle.load(cellFile)


time = yamada_data["time"]
v_yamada = yamada_data["voltage"]
channels_yamada = yamada_data["channels"]

v_hh = hh_data["voltage"]
channels_hh = hh_data["channels"]

cm = 1/2.54

fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(15*cm, 5*cm))
fig.set_tight_layout(20)

ax[0].plot(time, channels_hh['n_hh2'], color='red', label='Ativação canais $K^+$ ')
ax[0].set_ylabel('$n$')
ax[0].set_title('(A)', loc='left')

ax[1].plot(time, channels_yamada['m_im'], color='magenta', label='Ativação persistente\ncanais $K^+$ ')
ax[1].set_ylabel('$m$')
ax[1].set_title('(B)', loc='left')

for axis in ax:
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.set_ylim(-0.05,1.19)
    axis.legend(loc='upper right')
    axis.set_xlabel('Tempo (ms)', fontsize=9)


plt.savefig('plotPersistenteChannels.png',dpi=600, bbox_inches='tight', format='png')