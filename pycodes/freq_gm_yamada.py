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


with open(f'../results/gm_freq_YamadaHH.pkl', 'rb') as f:
    dados = pickle.load(f)

gms = dados['gms']
freqs_yamada_hz = dados['freqs_yamada_hz']

cm = 1/2.54
fig, ax = plt.subplots(figsize=(10*cm,8*cm))
ax.grid(alpha=0.3)
ax.scatter(x = gms*1e5, y = freqs_yamada_hz, alpha=0.1, s=2)
ax.scatter(x = gms[350]*1e5, y = freqs_yamada_hz[350], color = 'green', label='$g_{m}$ fixo neste trabalho', s=5)
ax.scatter(x = gms[0]*1e5, y = freqs_yamada_hz[0], color = 'red', label='Modelo Hodgkin-Huxley sem $I_M$', s=5 )
ax.set_ylabel('Frequência (Hz)')
ax.set_xlabel('$g_{m}$ ($m$ S/mm²)')
ax.set_xticklabels(["", "0", "0,01", "0,02", "0,03", "0,04", "0,05"])

ax.spines['right'].set_visible(False, )
ax.spines['top'].set_visible(False)
# ax.set_xlim(-0.05e-5,0.5*10e-5)
ax.set_xlim(-0.05, 5.5)
ax.legend()

ax.set_title('(E)', fontsize=20, pad=20, loc='left')

plt.savefig('gm_freq_YamadaHH.png', dpi=600, bbox_inches='tight', format='png')