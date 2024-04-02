import numpy as np
import matplotlib.pyplot as plt

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

# Constantes
C_m = 1.0  # Capacitância de membrana (uF/cm^2)
g_Na = 120.0  # Condutância máxima de sódio (mS/cm^2)
g_K = 36.0  # Condutância máxima de potássio (mS/cm^2)
g_L = 0.3  # Condutância máxima de fuga (mS/cm^2)
E_Na = 50.0  # Potencial de equilíbrio para o sódio (mV)
E_K = -77.0  # Potencial de equilíbrio para o potássio (mV)
E_L = -54.387  # Potencial de equilíbrio para a fuga (mV)

# Tempo de simulação
t_start = 0
t_end = 60
dt = 0.01
num_steps = int((t_end - t_start) / dt)

# Inicialização das variáveis
V_m = -65.0  # Potencial de membrana inicial (mV)
m = 0.05  # Variável de ativação de sódio inicial
h = 0.6  # Variável de inativação de sódio inicial
n = 0.32  # Variável de ativação de potássio inicial

# Parâmetros de estímulo
I = np.zeros(num_steps)
I[1000:2000] = 3.0  # Estímulo de corrente aplicado durante 1 ms
I[5000:7000] = 1.5  # Estímulo de corrente aplicado durante 1 ms
I[9000:9200] = 5.0  # Estímulo de corrente aplicado durante 1 ms
I[10200:10400] = 5.0  # Estímulo de corrente aplicado durante 1 ms
I[14000:14500] = 3.0  # Estímulo de corrente aplicado durante 1 ms

# Arrays para armazenar os resultados
V_m_values = np.zeros(num_steps)
m_values = np.zeros(num_steps)
h_values = np.zeros(num_steps)
n_values = np.zeros(num_steps)

# Loop de simulação
for i in range(num_steps):
    # Equações do modelo de Hodgkin-Huxley
    alpha_m = 0.1 * (V_m + 40.0) / (1.0 - np.exp(-(V_m + 40.0) / 10.0))
    beta_m = 4.0 * np.exp(-(V_m + 65.0) / 18.0)
    alpha_h = 0.07 * np.exp(-(V_m + 65.0) / 20.0)
    beta_h = 1.0 / (1.0 + np.exp(-(V_m + 35.0) / 10.0))
    alpha_n = 0.01 * (V_m + 55.0) / (1.0 - np.exp(-(V_m + 55.0) / 10.0))
    beta_n = 0.125 * np.exp(-(V_m + 65.0) / 80.0)

    m_inf = alpha_m / (alpha_m + beta_m)
    tau_m = 1.0 / (alpha_m + beta_m)
    h_inf = alpha_h / (alpha_h + beta_h)
    tau_h = 1.0 / (alpha_h + beta_h)
    n_inf = alpha_n / (alpha_n + beta_n)
    tau_n = 1.0 / (alpha_n + beta_n)

    dV_m = (I[i] - g_Na * m ** 3 * h * (V_m - E_Na) - g_K * n ** 4 * (V_m - E_K) - g_L * (V_m - E_L)) / C_m
    dm = (m_inf - m) / tau_m
    dh = (h_inf - h) / tau_h
    dn = (n_inf - n) / tau_n

    V_m += dt * dV_m
    m += dt * dm
    h += dt * dh
    n += dt * dn

    # Armazenamento dos resultados
    V_m_values[i] = V_m
    m_values[i] = m
    h_values[i] = h
    n_values[i] = n


# Plot dos resultados
cm = 1/2.54
fig, (ax, axi, axm, axh, axn) = plt.subplots(ncols=1, nrows=5,figsize=(15*cm, 20*cm), gridspec_kw={'height_ratios':[4,1.,1.2,1.2,1.2]})
fig.set_tight_layout(20)
axes = (ax, axi, axm, axh, axn)
graficos = [f'({i})' for i in ("A","B","C","D","E")]


t = np.arange(t_start, t_end, dt)
red = V_m_values > -60
blue = V_m_values < -60

# ax.annotate(text=r'\textit{Spike}', xy=(32,55), xytext=None)
# ax.annotate(text=r'\textit{Rest}', xy=(25,-55), xytext=None)
# ax.annotate(text=r'\textit{Rest}', xy=(45,-55), xytext=None)
inicio_desp, fim_desp = 1000, 1500
inicio_repo, fim_repo = 1500, 1750


ax.plot(t[:inicio_desp], V_m_values[:inicio_desp], color='black')
ax.plot(t[fim_repo:], V_m_values[fim_repo:], color='black')

ax.plot(t[inicio_desp:fim_desp], V_m_values[inicio_desp:fim_desp], color='red', label='despolarização', linestyle='dotted', linewidth=1.2)
ax.plot(t[inicio_repo:fim_repo], V_m_values[inicio_repo:fim_repo], color='blue', label='repolarização', linestyle='dashdot', linewidth=1.2)
ax.set_yticks(np.arange(-90, 120, 30))

axi.plot(t, I, color='black', label='Estímulo')

for i, axis in enumerate(axes):
    axis.set_title(graficos[i], loc='left')
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.set_xlim(5,25)

for axis in axes[:-1]:
    axis.get_xaxis().set_visible(False)


axes[-1].set_xlabel('Tempo (ms)')
ax.set_ylabel('$V_m$ (mV)')
axi.set_ylabel(r'$I_{ext} (\mu A/mm^2)$', fontsize=10)
# ax.set_title('Evolução do potencial de Membrana')

ax.set_ylim(-90,60)
ax.legend()
axi.legend()
# plt.grid(True)
# plt.show()

axm.plot(t[inicio_desp:fim_desp], m_values[inicio_desp:fim_desp], color='red', label=r'Abertura Canais Na$^+$')
axm.plot(t[fim_desp:fim_repo+100], m_values[fim_desp:fim_repo+100], color='magenta',linestyle='dashed', label=r'Fechamento Canais Na$^+$')
axm.plot(t, m_values, color='red', alpha=0.2)
axm.set_ylabel('m')

axh.plot(t[inicio_repo-50:fim_repo+500], h_values[inicio_repo-50:fim_repo+500], color='blue', label=r'Fechamento Canais Na$^+$')
axh.plot(t[:], h_values[:], color='blue', alpha=0.2)
axh.set_ylabel('h')

axn.plot(t[inicio_repo-50:fim_repo+500], n_values[inicio_repo-50:fim_repo+500], color='green', label=r'Abertura Canais K$^+$')
axn.plot(t[:], n_values[:], color='green', alpha =0.2)
axn.set_ylabel('n')


for axis in axes[2:]:
    axis.set_yticks([0,0.5,1])
    axis.set_yticklabels(['0','0,5','1'])
    axis.set_ylim(0,1)
    axis.legend(loc='upper right')


plt.savefig('evolucao_potencial_membrana_canais.png', dpi=600, bbox_inches='tight', format='png')


