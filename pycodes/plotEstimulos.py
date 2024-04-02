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

import numpy as np
import matplotlib.pyplot as plt

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
t_end = 120
dt = 0.01
num_steps = int((t_end - t_start) / dt)
t = np.arange(t_start, t_end, dt)

# Inicialização das variáveis
V_m = -65.0  # Potencial de membrana inicial (mV)
m = 0.05  # Variável de ativação de sódio inicial
h = 0.6  # Variável de inativação de sódio inicial
n = 0.32  # Variável de ativação de potássio inicial

# Parâmetros de estímulo
I = np.zeros(num_steps)
I[1000:1500] = 3.0  # Estímulo de corrente aplicado durante 1 ms
I[5000:7000] = 1.5  # Estímulo de corrente aplicado durante 1 ms
I[9000:9200] = 5.0  # Estímulo de corrente aplicado durante 1 ms
I[10200:10400] = 5.0  # Estímulo de corrente aplicado durante 1 ms
I[14000:] = 15.0  # Estímulo de corrente aplicado durante 1 ms

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


cm = 1/2.54

fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(16*cm, 12*cm))
fig.set_tight_layout(20)

ax[0].plot(t, V_m_values, color='black')
ax[1].plot(t, I, color='gray')

#titles
ax[0].set_title('(A)',loc='left')
ax[1].set_title('(B)',loc='left')

#labels
ax[0].set_ylabel('$V_m$ (mV)')
ax[1].set_ylabel('$I_{ext}$ ($\mu$A/mm$^2$)')
ax[1].set_xlabel('Tempo (ms)')


# spines 
ax[0].spines['top'].set_visible(False)
ax[1].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)
ax[1].spines['right'].set_visible(False)

# ticks 
ax[0].set_yticks(np.arange(-90, 100, 25))
ax[0].set_ylim(-90, 60)
ax[0].set_xlim(0, None)
ax[1].set_yticks(np.arange(0, 7, 1))
ax[1].set_ylim(-0.05, 6)
ax[1].set_xlim(0, None)

# Anotations
ax[1].annotate('(I)', xy=(10,4))
ax[1].annotate('(II)', xy=(56,2))
ax[1].annotate('(III)', xy=(93,5.5))
# ax[1].annotate('(VI)', xy=(139,4))

plt.savefig('plotEstimulos.png', dpi=600, bbox_inches='tight', format='png')
