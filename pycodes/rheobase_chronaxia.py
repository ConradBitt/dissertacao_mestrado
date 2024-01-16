import pickle
import numpy as np
from matplotlib import pyplot as plt, ticker
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

with open('../results/dados_reobase_chronaxia.pkl','rb') as pklfile:
    dados = pickle.load(pklfile)


chronaxie_percent_stimulus = dados['chronaxie_percent_stimulus']
i_exts = dados['i_exts']
frequencias = dados['frequencias']
cvs = dados['cvs']



cm = 1/2.54


fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12*cm, 10*cm))
fig.set_tight_layout(20)


tg, ig = np.meshgrid(i_exts*1000, chronaxie_percent_stimulus*100)

hm00 = ax.pcolor(ig, tg, frequencias, cmap='gnuplot2')
cbar00 = fig.colorbar(hm00, ax=ax)#, cax=cax1, format=formater)
cbar00.ax.set_title(r'$Fr$ (Hz)')

# hm01 = ax[1].pcolor(ig, tg, cvs, cmap='gnuplot2')
# cbar01 = fig.colorbar(hm01, ax=ax[1])#, cax=cax1, format=formater)
# cbar01.set_label(r'$\overline{CV}$')

ax.set_title('(A)', loc='left', pad=20)
# ax[1].set_title('(B)', loc='left', pad=20)

ax.set_xlabel('Tempo de estímulo \n(\% do tempo de simulação em ms)', fontsize=14)
# ax[1].set_xlabel('Tempo de estímulo (\% do tempo de simulação)', fontsize=12)

# vals0 = ax[0].get_xticks()
# ax[0].set_xticklabels(['{:,.2%}'.format(x) for x in vals0])
# vals1 = ax[0].get_xticks()
# ax[1].set_xticklabels(['{:,.2%}'.format(x) for x in vals1])

# ax[0].xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
# ax[1].xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

# ax[0].set_ylabel('$I_{ext}$ ($pA$)')
ax.set_ylabel('$I_{ext}$ ($pA$)')

ax.annotate('(I)', xy=(0,0), xytext=(20,100), color='white', fontsize=24)
ax.annotate('(II)', xy=(0,0), xytext=(80,150), color='black', fontsize=24)


plt.savefig('reobase_chronaxia.png', dpi=600, bbox_inches='tight', format='png')