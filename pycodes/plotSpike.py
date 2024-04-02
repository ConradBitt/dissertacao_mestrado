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
t_end = 150
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

cm = 1/2.54
fig, ax = plt.subplots(figsize=(10*cm, 6*cm))

# data
i_desp, f_desp = 1000,1480
i_repo, f_repo = f_desp, 1750

ax.plot(t[200:i_desp], V_m_values[200:i_desp], color='black')
ax.plot(t[i_desp:f_desp], V_m_values[i_desp:f_desp], color='red', linestyle='dotted', label='Despolarização')
ax.plot(t[i_repo:f_repo], V_m_values[i_repo:f_repo], color='blue', linestyle='dashdot', label='Repolarização')
ax.plot(t[f_repo:3000], V_m_values[f_repo:3000], color='black')

# visual 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.vlines(x=10, ymin=-500, ymax=80, linestyle='dashed', color='gray')
ax.vlines(x=17.5, ymin=-500, ymax=80, linestyle='dashed', color='gray')

#labels, ticks
ax.set_xlabel('Tempo (ms)')
ax.set_ylabel('$V_m$ (mV)')

ax.set_yticks(np.arange(-90, 80, 25))
ax.set_ylim(-90.05,75.05)
ax.set_xlim(5,30)

ax.annotate(r'\textit{Rest}', xy = (6, -55))
ax.annotate(r'\textit{Rest}', xy = (20, -55))
ax.annotate(r'\textit{Spike}', xy = (12.5, 60))

ax.legend()

plt.savefig('plotSpike.png', dpi=600, bbox_inches='tight', format='png')