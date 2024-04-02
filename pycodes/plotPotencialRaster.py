import pickle
import numpy as np
import matplotlib.colors as mcolors
# import matplotlib.ticker as plticker
import matplotlib.patches as patches
import locale
import sys
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

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

with open('../data/v0_batch0/v0_batch0_data.pkl','rb') as f:
    dados_1 = pickle.load(f)

with open('../data/v0_batch2/v0_batch2_data.pkl','rb') as f:
    dados_2 = pickle.load(f)


t = dados_1['simData']['t']
t2 = dados_2['simData']['t']

spkt = dados_1['simData']['spkt']
spkid = dados_1['simData']['spkid']
spkt2 = dados_2['simData']['spkt']
spkid2 = dados_2['simData']['spkid']

spkid = np.array(spkid)  # Converter para NumPy array
spkts = np.array(spkt)      # Converter para NumPy array
unique_gids = np.unique(spkid)
spkmat = [spkts[spkid == gid] for gid in unique_gids]

spkid2 = np.array(spkid2)  # Converter para NumPy array
spkts2 = np.array(spkt2)      # Converter para NumPy array
unique_gids2 = np.unique(spkid2)
spkmat2 = [spkts2[spkid2 == gid] for gid in unique_gids2]

cores = list(mcolors.TABLEAU_COLORS.keys())
# id_somas = np.arange(1,100, len(cores))
id_somas = [0,41,61,91]

v_21 = dados_1['simData']['V_soma']['cell_0']
v_41 = dados_1['simData']['V_soma']['cell_41']
v_61 = dados_1['simData']['V_soma']['cell_61']
v_91 = dados_1['simData']['V_soma']['cell_91']
lista_somas = [v_21, v_41, v_61, v_91]

v_21_2 = dados_2['simData']['V_soma']['cell_0']
v_41_2 = dados_2['simData']['V_soma']['cell_41']
v_61_2 = dados_2['simData']['V_soma']['cell_61']
v_91_2 = dados_2['simData']['V_soma']['cell_91']
lista_somas_2 = [v_21_2, v_41_2, v_61_2, v_91_2]


cm = 1/2.54

fig, ((ax0,ax2),(ax1,ax3)) = plt.subplots(ncols=2, nrows=2, figsize=(15*cm, 12*cm))
fig.set_tight_layout(20)
# gs = fig.add_gridspec(2, 1, height_ratios=[1,2])

# ax0 = fig.add_subplot(gs[0, 0])
ax0.set_title('(A)', loc='left', pad=10, fontsize=12)
ax0.xaxis.set_visible(False)
ax0.set_ylabel('Voltage (mV)', fontsize=10)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.hlines(y = 25, xmin=1900, xmax=2500, linestyles='--', colors='black', linewidth=1, label='limiar')
# ax0.spines['bottom'].set_visible(False)
j = 0
for soma in lista_somas:
    ax0.plot(t, soma, c= cores [j])
    j+=1
    
ax1.set_title('(B)', loc='left', pad=10, fontsize=12)
# ax1.xaxis.set_visible(False)
ax1.set_ylabel('$n$-ésimo neuronio', fontsize=10)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

j = 0
for i, t_peaks in zip(unique_gids,spkmat):
    if i in id_somas:
        ax1.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color=cores[j], s=12)
        j+=1
    else:
        ax1.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color='black', s=0.5)

#####################################
ax2.set_title('(C)', loc='left', pad=10, fontsize=12)
ax2.xaxis.set_visible(False)
ax2.set_ylabel('$V_m$ (mV)', fontsize=10)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.hlines(y = 25, xmin=1900, xmax=2500, linestyles='--', colors='black', linewidth=1, label='limiar')
# ax0.spines['bottom'].set_visible(False)
j = 0
for soma in lista_somas_2:
    ax2.plot(t2, soma, c= cores [j])
    j+=1

ax3.set_title('(D)', loc='left', pad=10, fontsize=12)
# ax1.xaxis.set_visible(False)
ax3.set_ylabel('$n$-ésimo neuronio', fontsize=10)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)

j = 0
for i, t_peaks in zip(unique_gids2,spkmat2):
    if i in id_somas:
        ax3.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color=cores[j], s=12)
        j+=1
    else:
        ax3.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color='black', s=0.5)


ti = 2250
tf = 2450

ax0.set_xlim(ti, tf)
ax1.set_xlim(ti, tf)
ax1.set_xlabel('Tempo (ms)', fontsize=10)
ax1.set_ylim(None, 100)

ax2.set_xlim(ti, tf)
ax3.set_xlim(ti, tf)
ax3.set_xlabel('Tempo (ms)', fontsize=10)
ax3.set_ylim(None, 100)


for axis in (ax0, ax2):
    axis.set_ylim(None, 75)
    axis.set_yticks(np.arange(-95,95,30))
    axis.set_yticklabels([str(i) for i in np.arange(-95,95,30)])

# anotações 
ax0.annotate(text='Disparo', xy=(2290, 80), xytext=(2290, 80), fontsize=9,color=cores[0])
ax0.annotate(text='Rajadas', xy=(2350, 80), xytext=(2350, 80), fontsize=9,color=cores[3])

# retangulos

## Defina os limites do retângulo
x_min01, x_max01 = 2300, 2325
y_min01, y_max01 = -85, 55

x_min02, x_max02 = 2352, 2388
y_min02, y_max02 = -85, 55

# retangulo
rect01 = patches.FancyBboxPatch((x_min01, y_min01), x_max01 - x_min01, y_max01 - y_min01, boxstyle="round,pad=0.5", edgecolor=cores[0], linestyle='dashed', linewidth=1, fill=None)
rect02 = patches.FancyBboxPatch((x_min02, y_min02), x_max02 - x_min02, y_max02 - y_min02, boxstyle="round,pad=0.5", edgecolor=cores[3], linestyle='dashed', linewidth=1, fill=None)

ax0.add_patch(rect01)
ax0.add_patch(rect02)


x_min11, x_max11 = 2300, 2325
y_min11, y_max11 = -5, 99

x_min12, x_max12 = 2352, 2388
y_min12, y_max12 = -5, 99


rect12 = patches.FancyBboxPatch((x_min12, y_min12), x_max12 - x_min12, y_max12 - y_min12, boxstyle="round,pad=0.5", edgecolor=cores[3], linestyle='dashed', linewidth=1, fill=None)

ax1.add_patch(rect12)


plt.savefig('plotPotencialRaster.png', dpi=1200, bbox_inches='tight', format='png')
