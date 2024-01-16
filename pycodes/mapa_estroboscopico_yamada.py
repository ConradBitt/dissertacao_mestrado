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
    # plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()


################################
#       Modelo
###############################
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definição das constantes do modelo de Hodgkin-Huxley
C = 1.0  # Capacitância da membrana (em uF/cm^2)
g_Na = 120.0  # Condutância máxima de sódio (em mS/cm^2)
g_K = 36.0  # Condutância máxima de potássio (em mS/cm^2)
g_leak = 0.3  # Condutância máxima de vazamento (em mS/cm^2)
V_Na = 50.0  # Potencial de reversão de sódio (em mV)
V_K = -77.0  # Potencial de reversão de potássio (em mV)
V_leak = -54.387  # Potencial de reversão de vazamento (em mV)

# Função que retorna as taxas de transição das variáveis de estado m, h e n
def alpha_m(V):
    # 0,1 \frac{V_m - 40}{ 1 - \expbr{-(V_m - 40)/10.0}}
    return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))

def beta_m(V):
    # 4,0 \expbr{-(V_m + 65) / 18}
    return 4.0 * np.exp(-(V + 65.0) / 18.0)

def alpha_h(V):
    # 0,07 * \expbr{(-(V_m + 65) / 20)}
    return 0.07 * np.exp(-(V + 65.0) / 20.0)

def beta_h(V):
    # \frac{1.0}{1 + \expbr{(-(V_m + 35) / 10)}}
    return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))

def alpha_n(V):
    #0,01 \frac{(V_m + 55)}{1 - \expbr{-(V_m + 55) / 10)}}
    return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))

def beta_n(V):
    # 0,125 \expbr[(-(V_m + 65) / 80)]
    return 0.125 * np.exp(-(V + 65.0) / 80.0)

# Função que retorna as derivadas das variáveis de estado m, h e n
def dMdt(V, m):
    return alpha_m(V) * (1.0 - m) - beta_m(V) * m

def dHdt(V, h):
    return alpha_h(V) * (1.0 - h) - beta_h(V) * h

def dNdt(V, n):
    return alpha_n(V) * (1.0 - n) - beta_n(V) * n

# Função que retorna as derivadas das variáveis de estado V, m, h e n
def dVdt_hh(X, t, I):
    V, m, h, n = X
    # I = 10.0  # Corrente injetada no neurônio (em uA/cm^2)
    
    INa = g_Na * (m ** 3) * h * (V - V_Na)
    IK = g_K * (n ** 4) * (V - V_K)
    Ileak = g_leak * (V - V_leak)
    
    dVdt = (1.0 / C) * (I - INa - IK - Ileak)
    dmdt = dMdt(V, m)
    dhdt = dHdt(V, h)
    dndt = dNdt(V, n)
    return [dVdt, dmdt, dhdt, dndt]

# Condições iniciais
V0 = -65.0
m0 = alpha_m(V0) / (alpha_m(V0) + beta_m(V0))
h0 = alpha_h(V0) / (alpha_h(V0) + beta_h(V0))
n0 = alpha_n(V0) / (alpha_n(V0) + beta_n(V0))
X0_hh = [V0, m0, h0, n0]

# Tempo de integração
t = np.linspace(0, 1000, 5000)  # Intervalo de 0 a 50 ms, com 1000 pontos
def hhModel(t,x, i):
    sol = odeint(dVdt_hh, x, t, args=(i, ))
    return sol

currents = np.linspace(2.20, 2.25, 2000)
v_max = np.zeros_like(currents)
var_v = {}
t = np.linspace(0, 1000, 50000)

for i, iext in enumerate(currents):
    v = hhModel(t, X0_hh, iext)
    v_max[i] = v[:,0].max()
    var_v[i] = {
        'v':v[:,0],
        'dvdt': np.diff(v[:,0])
    }

rheobase = currents[v_max<0].max()
idx_rheobase = len(v_max[v_max<0])

####################################
#           Plot
####################################
cm = 1/2.54

fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(26*cm, 10*cm))
fig.set_tight_layout(20)

ax[0].set_title('(A)',loc='left',pad=15)
ax[0].scatter(-1*currents[v_max<0], v_max[v_max<0], s=15, color='blue', alpha=0.5, label='Não atinge Rheobase')
ax[0].scatter(-1*currents[v_max>0], v_max[v_max>0], s=15, color='black', alpha=0.5, label='Atinge Rheobase')
ax[0].set_ylabel('Voltagem máxima (mV)')
ax[0].set_xlabel('$I_{ext}$ ($\mu A / mm^2$)', fontsize=12)
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].set_xlim(-2.2,-2.25)
ax[0].set_ylim(-75,60)
ax[0].legend()

ax[1].set_ylabel('$\\frac{dV_m}{dt}$\t', rotation=0)
for axis in ax[1:]:
    axis.set_xlabel('$V_m$')
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False) 

ax[1].set_title('(B)',loc='left',pad=15)

for i in range(len(currents)):
    if i <idx_rheobase:
        ax[1].plot(var_v[i]['v'][:-1], var_v[i]['dvdt'],linewidth=0.5, color='blue', alpha=0.8)
        ax[2].plot(var_v[i]['v'][:-1], var_v[i]['dvdt'],linewidth=0.5, color='blue', alpha=0.8)
    else:
        ax[1].plot(var_v[i]['v'][:-1], var_v[i]['dvdt'],linewidth=0.5, color='black', alpha=0.8)    
        ax[2].plot(var_v[i]['v'][:-1], var_v[i]['dvdt'],linewidth=0.5, color='black', alpha=0.8)

ax[2].set_title('(C)',loc='left',pad=15)

ax[1].annotate('(C)', xy=(0,0), xytext=(-70,1.5), color='red')
ax[1].hlines(y=0.5, xmin=-70,xmax=-50, color='red')
ax[1].hlines(y=-0.5, xmin=-70,xmax=-50, color='red')
ax[1].vlines(x=-70, ymin=-0.5,ymax=0.5, color='red')
ax[1].vlines(x=-50, ymin=-0.5,ymax=0.5, color='red')

# ax[1].set_xlim(-85, 55)
# ax[1].set_ylim(-10,60)

ax[2].set_xlim(-70,-50)
ax[2].set_ylim(-0.3,0.1,)
# for i in range(368):
    # ax[1].plot(var_v[i]['v'][:-1], var_v[i]['dvdt'],linewidth=0.5, color='blue', alpha=0.8)

ax[1].plot(var_v[i]['v'][-10:], var_v[i]['dvdt'][-10:],linewidth=0.5, color='black', alpha=0.8, label='Atinge Rheobase')
ax[1].legend()
ax[2].plot(var_v[i]['v'][:10], var_v[i]['dvdt'][:10],linewidth=0.5, color='blue', alpha=0.8, label='Não atinge Rheobase')

ax[2].legend()

plt.savefig('espaco_fase_hh_neuron_teste.png', dpi=600, bbox_inches='tight', format='png')