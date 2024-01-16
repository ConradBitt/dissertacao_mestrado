import numpy as np 
import scipy
import sys
import os
from numba import jit, float64

def get_size(file):
    """
    Retorna o tamanho em megabytes de um dicionário e seus valores.

    Args:
        file (string): caminho do arquivo.

    Returns:
        float: O tamanho do dicionário e seus valores em megabytes.

    Raises:
        None
    """
    try:
        file_stats = os.stat(file)
        file_size = file_stats.st_size
        print(f"File Size is {file_size / (1024 * 1024):.2f}MB")
    except FileNotFoundError:
        print("File not found.")

def get_numpy(data):
    """
    Converte os dados em formato de dicionário para matrizes NumPy.

    Args:
        data (dict): Dados no formato JSON armazenados em um tipo dicionário contendo informações sobre os valores de tensão de simulação.

    Returns:
        tuple: Uma tupla contendo um array NumPy representando os tempos e uma matriz NumPy representando os valores de tensão.
    """
    mapa = np.zeros((len(data['simData']['V_soma']), len(data['simData']['t'])))
    t = np.array(data['simData']['t'])
    for i, value in enumerate(data['simData']['V_soma'].values()):
        mapa[i] = value
    return t, mapa

@jit(nopython=True)
def phi(t, t0, t1):
    """
    Calcula a fase em radianos para um determinado tempo 't' em relação aos tempos 't0' e 't1'.

    Args:
    t (float): O tempo para o qual a fase deve ser calculada.
    t0 (float): O tempo de início do intervalo.
    t1 (float): O tempo de término do intervalo.

    Returns:
    float: O valor da fase em radianos.
    """
    return 2 * np.pi * (t - t0) / (t1 - t0)

@jit(nopython=True)
def calculate_t_range(spkinds, spkts, step=1):
    """
    Calcula o intervalo de tempo 't_range' e organiza os eventos de disparo em grupos de neurônios.

    Args:
    spkinds (array-like): Um array-like contendo as identificações de grupo para cada evento de disparo.
    spkts (array-like): Um array-like contendo os tempos dos eventos de disparo correspondentes.
    step (float, opcional): O tamanho do passo para o intervalo de tempo 't_range'. Padrão é 1.

    Returns:
    Tuple[list, ndarray]: Uma tupla contendo duas informações:
        1. Uma lista de listas 'spkmat', onde cada sublista contém os tempos de disparo de um grupo de neurônios.
        2. Um array NumPy 't_range' representando o intervalo de tempo entre o primeiro e o último evento de disparo.
    """
    spkinds = np.array(spkinds)  # Converter para NumPy array
    spkts = np.array(spkts)      # Converter para NumPy array
    
    unique_gids = np.unique(spkinds)
    spkmat = [spkts[spkinds == gid] for gid in unique_gids]

    t_first_spk = np.inf
    t_last_spk = -np.inf

    for spks in spkmat:
        if len(spks) > 0:
            min_spk = np.min(spks)
            max_spk = np.max(spks)
            t_first_spk = min(t_first_spk, min_spk)
            t_last_spk = max(t_last_spk, max_spk)

    t_range = np.arange(t_first_spk, t_last_spk, step)

    return spkmat, t_range 

@jit(nopython=True)
def calculate_phases(spkmat, t_range, ti=0, tf=-1):
    """
    Calcula as fases dos intervalos inter-disparos (ISIs) para um conjunto de eventos de disparo e um intervalo de tempo.

    Args:
    spkmat (list): Uma lista de listas, onde cada sublista contém os tempos de disparo de um grupo de neurônios.
    t_phase (ndarray): Um array NumPy representando o intervalo de tempo entre o primeiro e o último evento de disparo.

    Returns:
    ndarray: Uma matriz NumPy contendo as fases calculadas para cada grupo de neurônios em relação ao intervalo de tempo 't_range'.
    """
    phases = np.zeros((len(spkmat), len(t_range)))

    for n, peak in enumerate(spkmat):
        # para cada ISI do neurônio
        for t0, t1 in zip(peak[:-1], peak[1:]):
            for i, t in enumerate(t_range):
                if t0 < t < t1:
                    # calcula a fase phi e adiciona no array
                    phases[n, i] = phi(t, t0, t1)
    t_phase = t_range[ti:tf]
    phases = phases[:, ti:tf]

    spkmat_temp = []
    for peaks in spkmat:
        _ = peaks[(peaks > np.min(t_phase)) & (peaks < np.max(t_phase))]
        spkmat_temp.append(_)

    return t_phase, phases, spkmat_temp


@jit(nopython=True)
def kuramoto_param_global_order(spatial_phase_arr):
    """
    Calculates the global order parameter of Kuramoto for a set of spatial phases.

    Args:
        spatial_phase_arr (numpy.ndarray): Array representing the spatial phase distribution of neurons.

    Returns:
        float: Value of the global order parameter of Kuramoto.

    """
    n = len(spatial_phase_arr)
    somatorio = 0j  # Use um número complexo inicializado com zero
    for i in range(n):
        i = i % n
        somatorio += np.exp(1j * spatial_phase_arr[i])  # Use 1j para representar números complexos
    z = np.abs(somatorio) / n
    return z

@jit(nopython=True)
def kuramoto_param_local_order(spatial_phase_arr, delta):
    """
    Calculates the Kuramoto parameter order for a given spatial phase distribution.

    Args:
        spatial_phase_arr (numpy.ndarray): Array representing the spatial phase distribution of neurons.
        delta (int): Window of neighboring neurons to consider.

    Returns:
        numpy.ndarray: Array of Kuramoto parameter order values for each neuron.
    """
    n = len(spatial_phase_arr)
    z = np.zeros_like(spatial_phase_arr, dtype=float64)

    for i in range(n):
        somatorio = 0j  # Use um número complexo inicializado com zero
        for offset in range(-delta, delta + 1):
            j = (i + offset) % n
            somatorio += np.exp(1j * spatial_phase_arr[j])  # Use 1j para representar números complexos
        z[i] = np.abs(somatorio / (2 * delta + 1))
    return z

@jit(nopython=True)
def isi_cv_freq(tpeaks, ti=0,tf=-1):
    """
    Calcula o inter-spike-interval (ISI) de uma lista de tspikes.

    Args:
        tpeaks (list of arrays): A lista contendo n-arrays com o tempo em que ocorre os spikes.

    Returns:
        tupla: uma tupla contendo as seguintes matrizes:
             - isi_bar (numpy.ndarray): Matriz de ISIs médios para cada neurônio.
             - cv (numpy.ndarray): Matriz de coeficiente de variação (CV) dos ISIs para cada neurônio.
             - freq_bar (numpy.ndarray): Matriz de frequências médias de disparo (em Hz) para cada neurônio.
    """
    num_neurons = len(tpeaks)
    isi_bar = np.zeros(num_neurons)
    cv = np.zeros(num_neurons)
    freq_bar = np.zeros(num_neurons)
    
    for i in range(num_neurons):    
        nspikes = tpeaks[i][(tpeaks[i] > ti) & (tpeaks[i] < tf)]
        isis = np.empty(len(tpeaks[i]) - 1, dtype=np.float64)
        for j in range(len(tpeaks[i]) - 1):
            isis[j] = tpeaks[i][j + 1] - tpeaks[i][j]

        isi_bar[i] = np.mean(isis)
        freq_bar[i] = (1 / isi_bar[i]) * 1e3  # Convert ISI to firing frequency (Hz)
        cv[i] = np.std(isis) / isi_bar[i]
    
    return isi_bar, cv, freq_bar

def countNeuronsUnderThr(lop, thresholds):
    """
    Realiza a média temporal do lop dos neuronios, conta quantos elementos estão abaixo do threhold.

    Esta função recebe um conjunto de dados 'lop' representando séries temporais e uma lista de 'thresholds' (limiares).
    Ela realiza uma análise da média das séries temporais e conta o número de elementos coerentes,
    onde um elemento é considerado coerente se seu valor médio é menor do que um determinado limiar.

    Args:
        lop (numpy.ndarray): Um array NumPy contendo as séries temporais a serem avaliadas.
        thresholds (list of float): Uma lista de limiares para definir a coerência.

    Returns:
        tuple: Uma tupla contendo:
            - Um array NumPy representando a média das séries temporais (excluindo a última iteração).
            - Um array NumPy contendo o número de elementos coerentes para cada limiar.

    Raises:
        None
    """
    # Calcula o valor médio ao longo das séries temporais, excluindo a última iteração
    mean_lop_temporal = lop.mean(axis=1)
    
    # Inicializa um array para armazenar o número de elementos coerentes para cada limiar
    n_coerentes = np.zeros_like(thresholds)
    
    # Itera através dos limiares e conta o número de elementos coerentes
    for i, thr in enumerate(thresholds):
        n_coerentes[i] = len(mean_lop_temporal[mean_lop_temporal <= thr])
    
    return n_coerentes
