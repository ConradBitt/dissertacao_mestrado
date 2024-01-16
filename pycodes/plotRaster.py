import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
import sys

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    # plt.rcParams['mathtext.fontset'] = 'cm'
    # plt.rcParams['font.family'] = 'STIXGeneral'

def plotRaster(t_peaks, t_phase):
    cm = 1/2.54
    fig, ax = plt.subplots(figsize=(12*cm,6*cm))
    ax.set_title('(A)', loc='left', pad=20)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel('$n$-ésimo Neurônio')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylim(0, 256)
    ax.set_yticks(list(range(0,256, 50)),)
    ax.eventplot([event/1000 for event in t_peaks], color='black', linewidths=1,linestyles='-', zorder=3)
    ax.set_xlim(17, 20)
    # ax.set_xlim(min(t_phase), max(t_phase))
    # ax.xaxis.set_visible(False)


    plt.savefig(file+'_RasterPlot.png', dpi=600, bbox_inches='tight', format='png')

plot_params()



# v = str(sys.argv[1])
# i = str(sys.argv[2])
# j = str(sys.argv[3])
folder = f'../results/'
file = f'v4_batch1_23_29'

# file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
# file = f'../data/v0_batch0/v0_batch0'
print('~~ Plot Raster, LOP, Phase and GOP.')
print(f'Reading: "{file}"')

with open(folder+file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

cellNumber = data['simConfig']['cellNumber']
gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp'] * 1000
neighbours = data['simConfig']['n_neighbors']
freq_mean = data['freq_bar'].mean()
t_peaks = data['t_peaks']
t_phase = data['t_phase']

gop = data['GOP']
lop = data['LOP_delta'][5]

gop_sample = gop[:]
lop_sample = lop[:, :]

mean_lop = lop_sample.mean(axis=1)
last_lop = lop_sample[:, -10]

last_phases = data['phases'][:, -10]
t_sample = t_phase[:]

print(gop.shape, lop.shape, mean_lop.shape, last_lop.shape)

print(f'Plotting...')

plotRaster(t_peaks, t_phase)
# plotAll(t_peaks, last_phases, lop_sample, mean_lop, last_lop, t_sample, gop_sample)

print('\n~~')