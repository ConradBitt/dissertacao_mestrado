import pickle
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
# import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
import locale
import latex
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

# from matplotlib.colors import ListedColormap,LinearSegmentedColormap
# import matplotlib.cm
# gnuplot = matplotlib.cm.get_cmap('gnuplot')
# newcmp = ListedColormap(gnuplot(np.linspace(0.25, 0.75, 128)))

# newcmp = ListedColormap(viridis(np.linspace(0.25, 0.75, 128)))


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



v = 1
path = '../results_spaceparams/space_param_v2_batch1.pkl'
file = path.split('/')[-1].split('.')[0]
resol = 32
with open(path, 'rb') as f:
    data_space_param = pickle.load(f)

# cellNumber = data_space_param['infosNetWork']['cellNumber']
# amp = data_space_param['infosNetWork']['amp']
# neuronsPerCore = data_space_param['infosNetWork']['neuronsPerCore']
# coresPerNode = data_space_param['infosNetWork']['coresPerNode']

gex = data_space_param['gex']
neighbours = data_space_param['neighbours']
amp = data_space_param['amp']
mean_LOP = data_space_param['mean_LOP']
cluth75 = data_space_param['cluth75']
cluth80 = data_space_param['cluth80']
cluth85 = data_space_param['cluth85']
cluth90 = data_space_param['cluth90']
cluth95 = data_space_param['cluth95']
cluth100 = data_space_param['cluth100']


mean_LOP_arr = np.array(np.array_split(data_space_param['mean_LOP'], resol))
cluth75_arr = np.array(np.array_split(data_space_param['cluth75'], resol))
cluth80_arr = np.array(np.array_split(data_space_param['cluth80'], resol))
cluth85_arr = np.array(np.array_split(data_space_param['cluth85'], resol))
cluth90_arr = np.array(np.array_split(data_space_param['cluth90'], resol))
cluth95_arr = np.array(np.array_split(data_space_param['cluth95'], resol))
cluth100_arr = np.array(np.array_split( data_space_param['cluth100'], resol))


# axis
axis_gex = np.array(list(set(gex)))#.astype(int)
axis_amp = np.array(list(set(amp)))
axis_neighbours = np.array(list(set(neighbours)))#.astype(float)
axis_gex.sort()
axis_amp.sort()
axis_neighbours.sort()


print(mean_LOP_arr.shape)

fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(8,6))
fig.set_tight_layout(20)

# tg, ig = np.meshgrid(axis_neighbours[1:]/256, axis_gex[1:])
tg, ig = np.meshgrid(axis_amp[1:]*1000, axis_gex[1:])

ax[0][0].set_title('(A)', loc='left',pad=10)
hm00 = ax[0][0].pcolor(ig, tg, cluth80_arr, cmap='gnuplot')
cbar00 = fig.colorbar(hm00, ax=ax[0][0])#, cax=cax1, format=formater)
cbar00.ax.set_title(r'$Q(0,80)$')

# ax[0][1].set_title('$\overline{\overline{LOP}(t)}$')
ax[0][1].set_title('(B)', loc='left',pad=10)
hm01 = ax[0][1].pcolor(ig, tg, cluth85_arr, cmap='gnuplot')
cbar01 = fig.colorbar(hm01, ax=ax[0][1])#, cax=cax1, format=formater)
cbar01.ax.set_title(r'$Q(0,85)$')

# ax[1][0].set_title('$\overline{Fr}$')
ax[1][0].set_title('(C)', loc='left',pad=10)
hm03 = ax[1][0].pcolor(ig, tg, cluth90_arr, cmap='gnuplot')
cbar03 = fig.colorbar(hm03, ax=ax[1][0])#, cax=cax1, format=formater)
cbar03.ax.set_title(r'$Q(0,90)$')

# ax[1][1].set_title('$\overline{CV}$')
ax[1][1].set_title('(D)',loc='left',pad=10)
hm02 = ax[1][1].pcolor(ig, tg, cluth95_arr, cmap='gnuplot')
cbar02 = fig.colorbar(hm02, ax=ax[1][1])#, cax=cax1, format=formater)
cbar02.ax.set_title(r'$Q(0,95)$')

step_y = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals
step_x = plticker.MultipleLocator(base=0.5e-4)

# for linha in ax:
#     for coluna in linha:
#         coluna.yaxis.set_major_locator(step_y)
#         coluna.xaxis.set_major_locator(step_x)
#         coluna.set_ylim(None,0.36)
#         coluna.set_xlim(None,4.e-4)

ax[0][0].set_ylabel('$I_{ext}$ ($pA$)')
ax[1][0].set_ylabel('$I_{ext}$ ($pA$)')

# ax[0][0].set_ylabel('$r$')
# ax[1][0].set_ylabel('$r$')
ax[1][0].set_xlabel('$g_{ex}$ ($mS/cm²$)')
ax[1][1].set_xlabel('$g_{ex}$ ($mS/cm²$)')

plt.savefig(f'{file}_counts.png', dpi=600, bbox_inches='tight', format='png')
plt.show()