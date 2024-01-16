import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
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
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()


###################### Simulação:

# gm = 3.5e-5
# iext = 0.170
# tf = 2000
# dur = 1800
# delay = 100
# nome = 1
# python3 createCell.py gm tf amp dur delay nome
# os.system(f'python3 createCell.py {gm} {tf} {iext} {dur} {delay} {nome}')
# with open(f'cell{nome}.pkl','rb') as cell:
#     dados = pickle.load(cell)
# time = dados["time"]
# voltage = dados["voltage"]
# stim_current = dados["stim_current"]
# channels = dados["channels"]

label = ['alpha', 'beta', 'gamma']
cores = ['red', 'green', 'blue']
letras = ['(A)', '(B)', '(C)', '(D)']
gm_iext = [(0.1e-5,170), (3.5e-5,170), (4.7e-5,170)]
tf = 5000
dur = 4000
delay = 500


dados = {}
for letra, par in zip(label, gm_iext):
    gm, iext = par

    os.system(f'python3 createCell.py {gm} {tf} {iext/1000} {dur} {delay} {letra}')
    with open(f'cell{letra}.pkl','rb') as cellFile:
        cell = pickle.load(cellFile)
    time = cell["time"]
    voltage = cell["voltage"]
    stim_current = cell["stim_current"]
    channels = cell["channels"]

    dados[letra] = time, voltage, stim_current, channels



#------------------------------------------------------------------------------
# Plot figure
#------------------------------------------------------------------------------
# f, (ax0, ax1) = plt.subplots(2,1, figsize=(10,3),
#                               gridspec_kw = {'height_ratios':[3, 1]})


# ax0.set_ylabel('Voltage (mV)')
# ax0.spines['right'].set_visible(False)
# ax0.spines['top'].set_visible(False)
# ax0.spines['bottom'].set_visible(False)
# ax0.get_xaxis().set_visible(False)

# sns.lineplot(x = time, y =voltage, color='black', ax=ax0)
# ax1.plot(time,stim_current, 'gray')
# ax1.plot([0,0],[0,0.15],'k')
# ax1.text(20,0.125,f'{stim_current.max()}nA',va='center')
# ax1.set_ylabel('I (nA)')
# ax1.set_xlabel('t (ms)')

# ax1.spines['right'].set_visible(False)
# ax1.spines['top'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.get_yaxis().set_visible(False)
# plt.tight_layout()
cm = 1/2.54

f, ax = plt.subplots(4,1,figsize=(10*cm,12*cm),gridspec_kw = {'height_ratios':[4, 4, 4, 2]})
f.set_tight_layout(20)
ax_alpha, ax_betta, ax_gamma, ax_iext = ax

ax_potenciais = (ax_alpha, ax_betta, ax_gamma)

ax_iext.plot(time,stim_current, 'gray')
ax_iext.plot([0,0],[0,0.2],'k')
ax_iext.text(2300,stim_current.max()+50e-3,f'170pA',va='center')
ax_iext.set_ylabel('$I_{ext}$ (pA)')
ax_iext.set_xlabel('Tempo (ms)')
ax_iext.spines['right'].set_visible(False)
ax_iext.spines['top'].set_visible(False)
ax_iext.spines['left'].set_visible(False)
# ax_iext.get_yaxis().set_visible(False)
ax_iext.set_yticklabels([0, '', ''])
ax_iext.set_xlim(1,5500)

i = 0
for letra, dado in dados.items():
    time, voltage,_, _ = dado
    sns.lineplot(x = time, y = voltage, color=cores[i], ax=ax_potenciais[i], label=f'$\{letra}$')
    if i == 0:
        ax_potenciais[i].set_ylabel('Voltage (mV)', fontsize=12)
    ax_potenciais[i].spines['right'].set_visible(False)
    ax_potenciais[i].spines['top'].set_visible(False)
    ax_potenciais[i].spines['bottom'].set_visible(False)
    ax_potenciais[i].get_xaxis().set_visible(False)
    ax_potenciais[i].set_xlim(1,5500)
    ax_potenciais[i].set_ylim(None,95)
    ax_potenciais[i].legend(loc='upper right')
    i+=1
i = 0

ax[0].set_title('(A)', loc='left')
ax[1].set_title('(B)', loc='left')
ax[2].set_title('(C)', loc='left')
ax[3].set_title('(D)', loc='left')





#------------------------------------------------------------------------------
# Save figure
#------------------------------------------------------------------------------
fname = f'potencial_{iext/1000}pA_{gm}msCm2'
plt.savefig(fname + '.png', dpi=600, bbox_inches='tight', format='png')