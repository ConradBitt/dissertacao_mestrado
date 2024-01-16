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
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()

with open('../results/gm_iext_frequencia_yamada.pkl','rb') as pklfile:
    dados_freq_cv_yamada = pickle.load(pklfile)

gms = dados_freq_cv_yamada['gms']
i_exts = dados_freq_cv_yamada['i_exts']
frequencias = dados_freq_cv_yamada['frequencias']
cvs = dados_freq_cv_yamada['cvs']

cm = 1/2.54


fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(25*cm, 10*cm))
fig.set_tight_layout(20)


tg, ig = np.meshgrid(i_exts*1000, gms*1e3)

hm00 = ax[0].pcolor(ig, tg, frequencias, cmap='gnuplot2')
cbar00 = fig.colorbar(hm00, ax=ax[0])#, cax=cax1, format=formater)
cbar00.set_label(r'$Fr$ (Hz)')

hm01 = ax[1].pcolor(ig, tg, cvs, cmap='gnuplot2')
cbar01 = fig.colorbar(hm01, ax=ax[1])#, cax=cax1, format=formater)
cbar01.set_label(r'$\overline{CV}$')

ax[0].set_title('(A)', loc='left', pad=20)
ax[1].set_title('(B)', loc='left', pad=20)

ax[0].set_xlabel('$g_{M}$ ($mS/cm^2$)')
ax[1].set_xlabel('$g_{M}$ ($mS/cm^2$)')

ax[0].set_ylabel('$I_{ext}$ ($pA$)')


#região (I)
ax[0].annotate('(I)', xy=(6e-2,120),  color='white', fontsize=24)
# ax[1].annotate('(I)', xy=(6e-2,120),  color='white', fontsize=24)

#região (II)
ax[0].annotate('(II)', xy=(2e-2,140), color='white', fontsize=24)  
ax[1].annotate('(II)', xy=(2e-2,140), color='white', fontsize=24)  

ax[0].annotate(r'($\alpha$)', xy=(0.1e-2,170), color='black', fontsize=18)
ax[1].annotate(r'($\alpha$)', xy=(0.1e-2,170), color='white', fontsize=18)  

ax[0].annotate(r'($\beta$)', xy=(3.5e-2,170), color='white', fontsize=18)
ax[1].annotate(r'($\beta$)', xy=(3.5e-2,170), color='white', fontsize=18)  

ax[0].annotate(r'($\gamma$)', xy=(4.5e-2,170), color='white', fontsize=18)
ax[1].annotate(r'($\gamma$)', xy=(4.5e-2,170), color='white', fontsize=18)  

# (0.1e-2,170), (4.2e-2,170), (5.6e-2,170)
# gms*1e3 *e-2

for axis in ax:
    axis.set_ylim(75,200)
    axis.set_xlim(None, 5.1e-2)


plt.savefig('gm_iext_frequencia_yamada.png', dpi=600, bbox_inches='tight', format='png')