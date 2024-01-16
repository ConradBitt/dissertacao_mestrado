import os
import numpy as np
import scipy
from matplotlib import pyplot as plt, ticker
import neuron as nrn # NEURON simulator 
import sys
import os
from numba import jit, float64

# os.chdir('PospischilEtAl2008')
os.system('nrnivmodl') 
nrn.h.load_file("mosinit.hoc")
nrn.h.load_file("demo_PY_IBR.hoc")
# os.chdir('..')

def create_soma(verbose=False):
    soma = nrn.h.Section(name='soma')
    soma.nseg = 1 #
    soma.diam = 96 #
    soma.L = 96 #			// so that area is about 29000 um2
    soma.cm = 1 #
    soma.Ra = 100 #		// geometry

    if verbose:
        print("- Soma object:", soma)
        print("- Number of segments in the soma:", soma.nseg)
        print(f'- Diam: {soma.diam} | L: {soma.L} | cm: {soma.cm} | Ra: {soma.Ra}')
    return soma

def insert_mechanisms(soma, hh2=True, pas=True, im=True, it=True, il=True, return_mechs = False):
    if pas:
        soma.insert('pas')
        soma.e_pas = -85
        soma.g_pas = 1e-5 #		// idem TC cell

    if hh2:
        soma.insert('hh2'); #		// Hodgin-Huxley INa and IK
        soma.ek = -100 #		// potassium reversal potential
        soma.ena = 50 #			// sodium reversal potential
        soma.vtraub_hh2 = -55 #	// Resting Vm, BJ was -55
        soma.gnabar_hh2 = 0.05 #	// McCormick=15 muS, thal was 0.09
        soma.gkbar_hh2 = 0.005 #	// spike duration of pyr cells
        celsius = 36
        v_init = -84

    if im:
        soma.insert('im'); #		// M current
        taumax_im = 1000
        soma.gkbar_im = im#3e-5 #		// specific to LTS pyr cell

    if it:
        soma.insert('it'); #// IT current
        soma.cai = 2.4e-4
        soma.cao = 2
        #eca = 120
        soma.gcabar_it = 0.0004 #// specific to LTS pyr cell

    if il:
        soma.insert('ical'); #// IL current (Reuveni et al. model, Nernst)
        soma.cai = 2.4e-4
        soma.cao = 2
        #soma.eca = 120
        soma.gcabar_ical = 2.2e-4

        soma.insert('cad');  #		// calcium decay
        soma.depth_cad = 1 #		// McCormick= 0.1 um
        soma.taur_cad = 5 #		// McCormick=1 ms !!!
        soma.cainf_cad = 2.4e-4 #	// McCormick=0
        soma.kt_cad = 0 #		// no pump
        soma.depth_cad = 1 #		// McCormick= 0.1 um


    if return_mechs:
        return soma, hh2, pas, im, it, il
    else:
        return soma

def simConfig(soma, t, amp, dur, delay, return_channels=False, verbose=False):
    # Simulations Config
    ## Runs:
    nrn.h.tstop = t
    nrn.h.dt = 0.01

    iclamp = nrn.h.IClamp(.5, sec=soma)
    iclamp.amp = amp # nA
    iclamp.delay = delay # ms
    iclamp.dur = dur # ms

    #### Vectors
    time = nrn.h.Vector()
    voltage = nrn.h.Vector()
    stim_current = nrn.h.Vector()

    time.record(nrn.h._ref_t)
    voltage.record(soma(.5)._ref_v);
    stim_current.record(iclamp._ref_i)

    mechs_ionic = {}
    for mechs, param_mechs in soma.psection()['density_mechs'].items():
        for key_mechs in param_mechs.keys():
            if key_mechs in ['m','n','h']:
                # find the mechanisms and create a vector to record data.
                mechs_ionic[f'{key_mechs}_{mechs}'] = nrn.h.Vector()

    channels = {}
    for channel, mechs in mechs_ionic.items():
        # for every ionic mechanism, get the attribute and record it
        ref_record = getattr(soma(.5), f'_ref_{channel}')
        channels[channel] = mechs.record(ref_record);
        if verbose:
            print(f'--> mechanism {mechs_ionic} of soma is recorded...')

    if verbose:
        print("- Simulation stop time: %f ms" % nrn.h.tstop)
        print("- Integration time step: %f ms" % nrn.h.dt)
        print("- Amplitude external current: %f nA" % iclamp.amp)
        print("- Duration external current: %f ms" % iclamp.dur)
        print("- Delay external current: %f ms" % iclamp.delay)
        print('- Return Channels: ', return_channels)
    nrn.h.run()

    if return_channels:
        return time, voltage, stim_current, channels
    else:
        return time, voltage, stim_current
    

# def isi_cv_freq(tpeaks):
#     """
#     Calcula o inter-spike-interval (ISI) de uma lista de tspikes.

#     Args:
#         tpeaks (list of arrays): A lista contendo n-arrays com o tempo em que ocorre os spikes.

#     Returns:
#         tupla: uma tupla contendo as seguintes matrizes:
#              - isi_bar (numpy.ndarray): Matriz de ISIs médios para cada neurônio.
#              - cv (numpy.ndarray): Matriz de coeficiente de variação (CV) dos ISIs para cada neurônio.
#              - freq_bar (numpy.ndarray): Matriz de frequências médias de disparo (em Hz) para cada neurônio.
#     """
#     num_neurons = len(tpeaks)
#     isi_bar = np.zeros(num_neurons)
#     cv = np.zeros(num_neurons)
#     freq_bar = np.zeros(num_neurons)
    
#     for i in range(num_neurons):
#         isis = np.empty(len(tpeaks[i]) - 1, dtype=np.float64)
        
#         for j in range(len(tpeaks[i]) - 1):
#             isis[j] = tpeaks[i][j + 1] - tpeaks[i][j]

#         isi_bar[i] = np.mean(isis)
#         freq_bar[i] = (1 / isi_bar[i]) * 1e3  # Convert ISI to firing frequency (Hz)
#         cv[i] = np.std(isis) / isi_bar[i]
    
#     return isi_bar, cv, freq_bar

def isi_cv_freq(tpeaks):
    num_neurons = len(tpeaks)
    isi_bar = np.zeros(num_neurons)
    cv = np.zeros(num_neurons)
    freq_bar = np.zeros(num_neurons)
    
    for i in range(num_neurons):
        if len(tpeaks[i]) > 1:
            isis = np.empty(len(tpeaks[i]) - 1, dtype=np.float64)
            
            for j in range(len(tpeaks[i]) - 1):
                isis[j] = tpeaks[i][j + 1] - tpeaks[i][j]

            isi_bar[i] = np.mean(isis)
            freq_bar[i] = (1 / isi_bar[i]) * 1e3  # Convert ISI to firing frequency (Hz)
            cv[i] = np.std(isis) / isi_bar[i]
    
    return isi_bar, cv, freq_bar

def find_peaks(t_arr, v_arr, only_id=False):
    """
    Encontra os picos em um sinal de forma de onda.

    Args:
        t_arr (array-like): Uma matriz de tempos correspondentes aos valores do sinal de forma de onda.
        v_arr (array-like): Uma matriz de valores do sinal de forma de onda.
        only_id (bool, optional): Indica se apenas os IDs dos picos devem ser retornados. O padrão é False.

    Returns:
        tuple or numpy.ndarray: Se only_id for False, retorna uma tupla contendo os IDs dos picos, tempos correspondentes e valores correspondentes. Se only_id for True, retorna apenas os IDs dos picos.
    """
    peaks_id, _ = scipy.signal.find_peaks(v_arr, height=0)
    t = t_arr[peaks_id]
    v = v_arr[peaks_id]
    if only_id:
        peaks_id
    else:
        return peaks_id, t, v


def createCell(im, tf, amp, dur, hh2=True, pas=True):
    soma = create_soma()
    soma = insert_mechanisms(soma, hh2=True, pas=True, im=False, il=False, it=False)
    time, voltage, stim, channels = simConfig(soma, tf, amp, dur, 0, return_channels=True)
    return time, voltage, stim, channels 


###################### Simulação:
time, voltage, _, _ = createCell(3e-5, 2000, 0.170, 1000)

# currents = np.linspace(0, 0.250, 64)
# porcentagem_estimulo = np.linspace(0,1,64)

# frequencias = np.zeros((len(currents), len(porcentagem_estimulo)))
# cvs = np.zeros((len(currents), len(porcentagem_estimulo)))

# tf = 1000

# for i, iext in enumerate(currents):
#     for j, p, in enumerate(porcentagem_estimulo):
#         time, voltage, _, _ = createCell(3e-5, 2000, iext, p*1000)

    
#         _, t_peaks, _ = find_peaks(np.array(time), np.array(voltage))
#         _, cv, freq_bar = isi_cv_freq([t_peaks])
#         cv = cv.mean()
#         freq_bar = freq_bar.mean()
#         frequencias[i,j] = freq_bar
#         cvs[i,j] = cv

# dados = {
#     'chronaxie_percent_stimulus' : porcentagem_estimulo, 
#     'i_exts' : currents, 
#     'frequencias' : frequencias, 
#     'cvs' : cvs
# }

# import pickle
# with open('../../../results/dados_reobase_chronaxia.pkl', 'wb') as handle:
#     pickle.dump(dados, handle, protocol=pickle.HIGHEST_PROTOCOL)