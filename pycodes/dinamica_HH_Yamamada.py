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

path1 = f'../notebooks/one_cell/data_soma1.pkl'
path2 = f'../notebooks/one_cell/data_soma2.pkl'

with open(path1, 'rb') as f:
    data1 = pickle.load(f)

with open(path2, 'rb') as f:
    data2 = pickle.load(f)

with open('../results/dados_freq_hh_ym.pkl','rb') as f:
    dado_freq = pickle.load(f)

frq_hh = dado_freq['frq_hh']
frq_ym = dado_freq['frq_ym']
correntes = dado_freq['correntes']

time1 = data1['time']
voltage1 = data1['voltage']
stim1 = data1['stim']
channels1 = data1['channels']

time2 = data2['time']
voltage2 = data2['voltage']
stim2 = data2['stim']
channels2 = data2['channels']


import matplotlib.gridspec as gridspec
import seaborn as sns 
plot_params()
cm = 1/2.54

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(20*cm, 10*cm))
gs = gridspec.GridSpec(ncols=2, nrows=2, width_ratios=[2,1.8])
fig.set_tight_layout(10)

ax1 = plt.subplot(gs[:, 1])

for ax in axs[:,0]:
    ax.set_xlim(3000,4000)
    ax.set_ylim(-90,60)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel('Voltagem (mV)')
    
axs[0][0].set_title('(A)', loc='left')
axs[0][0].plot(time1, voltage1, color='black')
axs[1][0].plot(time2, voltage2, color='black')
axs[1][0].set_title('(B)', loc='left')
axs[1][0].set_xlabel('Tempo (ms)')



ax1.scatter(correntes*1000, frq_hh, color='blue', s=1)
ax1.scatter(correntes*1000, frq_ym, color='orange', s=1)
sns.lineplot(x = correntes*1000, y = frq_hh, color='blue', ax=ax1, label='Modelo Hodgkin-Huxley')
sns.lineplot(x = correntes*1000, y = frq_ym, color='red', ax=ax1 , label='Modelo Yamada')

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax1.set_title('(C)', loc='left')
ax1.set_ylabel('Frequência (Hz)')
ax1.set_xlabel('$I_{ext}$ ($p$A)')

ax1.set_xlim(0,800)

plt.savefig('dinamica_HH_Yamamada.png', dpi=600, bbox_inches='tight', format='png')





