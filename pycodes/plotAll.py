import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
import sys

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  

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
    # plt.rcParams['mathtext.fontset'] = 'cm'
    # plt.rcParams['font.family'] = 'STIXGeneral'

plot_params()

def plotAll(t_peaks, last_phases, lop_sample, mean_lop, last_lop, t_phase, gop_sample):
    fig, ax = plt.subplots(2,3, figsize=(10,6), gridspec_kw={'width_ratios':[5,1,1], 'height_ratios': [4,2] })
    np.random.seed(2788590720)
    indices_sorteados = np.random.choice(lop_sample.shape[1], 150)
    n = np.arange(lop_sample.shape[0])
    fig.set_tight_layout(15)
    infos = f'{int(gex*1e6)}$\mu$S/cm² | {amp:.1f}pA | {neighbours} Conns. | {int(freq_mean)}Hz'
    ax[0][0].set_title('(A) Raster Plot\n'+infos, loc='left', pad=20)
    ax[0][0].spines['right'].set_visible(False)
    ax[0][0].spines['top'].set_visible(False)
    # ax[0][0].set_title('$g_{ex}: '+f'{gex}$ S/cm²' + '\n'+'$I: '+f'{int(amp):.1f}$ pA'+ '\n' + f'Total Neighbors: {int(neighbours)}' +'\n' +f'Fr: {freq_mean:.2f}Hz', fontsize=11, loc='left', pad=20)
    ax[0][0].set_ylabel('$n$-ésimo Neurônio')
    ax[0][0].set_ylim(0, len(t_peaks))
    ax[0][0].eventplot(t_peaks, color='black')
    ax[0][0].xaxis.set_visible(False)

    # ax[0][0].set_xlim(min(t_phase),max(t_phase))
    # ax[1][0].set_xlim(min(t_phase), max(t_phase))

    for axis in (ax[0][0],ax[1][0]):
        axis.set_xlim(1.8e4, 2.e4)

    # ax[0][1].set_title(f'(B) $\phi$({str(int(t_sample[-1]))[:1]}s)', loc='left', pad=20)
    ax[0][1].set_title('(B) $\phi(t)$', loc='left', pad=20)
    ax[0][1].scatter(x = last_phases, y=n, color='green', s = 0.1)
    ax[0][1].set_xticks([0,2*np.pi])
    ax[0][1].set_xticklabels(['0','$2\pi$'])
    ax[0][1].set_xlabel('$\phi$(t)', fontsize=11)
    ax[0][1].spines['right'].set_visible(False)
    ax[0][1].spines['top'].set_visible(False)
    ax[0][1].yaxis.set_visible(False)

    ax[0][2].set_title('(C) LOP$(t)$',loc='left', pad=20)
    for lop in lop_sample[:, indices_sorteados].T:
        ax[0][2].scatter(x = lop, y = n, color='blue', alpha=0.005)
    ax[0][2].scatter(x = last_lop, y = n, s = 0.1, color='blue', label='LOP(t)')
    ax[0][2].scatter(x = mean_lop, y = n, s = 0.2, color='red', alpha=1, label='$\overline{LOP(t)}$')

    ax[0][2].set_xlim(0,1)
    ax[0][2].spines['right'].set_visible(False)
    ax[0][2].spines['top'].set_visible(False)
    ax[0][2].yaxis.set_visible(False)
    ax[0][2].legend(loc='lower left',fontsize="5")
    # ax[0][2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
    #         fancybox=True, shadow=True, ncol=1)


    ax[1][0].set_title('(D) Parametro Ordem Global', loc='left', pad=20)
    ax[1][0].plot(t_phase, gop_sample, color='darkred', label='GOP$(t)$')
    ax[1][0].spines['right'].set_visible(False)
    ax[1][0].spines['top'].set_visible(False)
    ax[1][0].set_ylim(-0.05, 1.05)
    ax[1][0].set_ylabel('GOP')
    ax[1][0].set_xlabel('Tempo (ms)')
    ax[1][0].legend(loc='upper right')


    ax[1][1].yaxis.set_visible(False)
    ax[1][1].xaxis.set_visible(False)
    ax[1][1].spines['right'].set_visible(False)
    ax[1][1].spines['left'].set_visible(False)
    ax[1][1].spines['top'].set_visible(False)
    ax[1][1].spines['bottom'].set_visible(False)

    ax[1][2].yaxis.set_visible(False)
    ax[1][2].xaxis.set_visible(False)
    ax[1][2].spines['right'].set_visible(False)
    ax[1][2].spines['top'].set_visible(False)
    ax[1][2].spines['left'].set_visible(False)
    ax[1][2].spines['bottom'].set_visible(False)

    print('->'+f'../AnalysisV{v}_n{len(n)}_{gex}Scm2_{amp:.1f}pA_r{neighbours/cellNumber:.2f}neigh_{int(freq_mean)}Hz.png')
    # plt.savefig(folder+f'AnalysisV{v}_n{len(n)}_{gex}Scm2_{amp:.1f}pA_r{neighbours/cellNumber:.2f}neigh_{int(freq_mean)}Hz.png', dpi=600, bbox_inches='tight', format='png')
    plt.savefig(folder+f'v{v}_batch1_{i}_{j}.png', dpi=600, bbox_inches='tight', format='png')

v = str(sys.argv[1])
i = str(sys.argv[2])
j = str(sys.argv[3])
folder = f'../figuresV2/'
file = f'../figuresV2/v{v}_batch1_{i}_{j}'

# file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
# file = f'../data/v0_batch0/v0_batch0'
print('~~ Plot Raster, LOP, Phase and GOP.')
print(f'Reading: "{file}"')

with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

cellNumber = data['simConfig']['cellNumber']
gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp'] * 1000
neighbours = data['simConfig']['n_neighbors']
freq_mean = data['freq_bar'].mean()
t_peaks = data['t_peaks']
t_phase = data['t_phase']
cv = data['cv']
print(cv.shape)
# gop = data['GOP']
# lop = data['LOP_delta'][5]

# gop_sample = gop[:]
# lop_sample = lop[:, :]

# mean_lop = lop_sample.mean(axis=1)
# last_lop = lop_sample[:, -10]

# last_phases = data['phases'][:, -10]
# t_sample = t_phase[:]

# print(gop.shape, lop.shape, mean_lop.shape, last_lop.shape)

# print(f'Plotting...')
# plotAll(t_peaks, last_phases, lop_sample, mean_lop, last_lop, t_sample, gop_sample)

# print('\n~~')