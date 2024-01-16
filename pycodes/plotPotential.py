"""
plot_potential.py 

File to plot json data of simulations fast-spiking neurons

Contributors: conradinho@gmail.com, fernandodasilvaborges@gmail.com
"""

import pickle
import seaborn as sns
import numpy as np

from matplotlib import pyplot as plt
sns.set_context('paper')

#------------------------------------------------------------------------------
# Read data
#------------------------------------------------------------------------------
with open('../data/v4_batch0002/v4_batch0002_0_1_data.pkl','rb') as file:
    v0_batch0_data = pickle.load(file) 

#------------------------------------------------------------------------------
# Set arrays
#------------------------------------------------------------------------------
gex = v0_batch0_data['simConfig']['gex']
amp = v0_batch0_data['simConfig']['IClamp0']['amp']
dur = v0_batch0_data['simConfig']['IClamp0']['dur']
start = v0_batch0_data['simConfig']['IClamp0']['start']
recordStep = v0_batch0_data['simConfig']['recordStep']

voltage = np.array(list(v0_batch0_data['simData']['V_soma'].values())[50])
time = np.array(v0_batch0_data['simData']['t'])
stim_current = np.array([0 if x < start/recordStep or x > (dur+start)/recordStep else amp for x in range(0, len(time))])


#------------------------------------------------------------------------------
# Plot figure
#------------------------------------------------------------------------------
f, (ax0, ax1) = plt.subplots(2,1, figsize=(10,3), gridspec_kw = {'height_ratios':[3, 1]})
sns.lineplot(x = time, y =voltage, color='black', ax=ax0)
ax1.plot(time,stim_current, 'gray')

ax0.set_ylabel('Voltage (mV)')
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.get_xaxis().set_visible(False)


ax1.plot([0,0],[0,0.15],'k')
ax1.text(20,0.125,f'{stim_current.max()}nA',va='center')
ax1.set_ylabel('I (nA)')
ax1.set_xlabel('t (ms)')

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.get_yaxis().set_visible(False)
plt.tight_layout()

#------------------------------------------------------------------------------
# Save figure
#------------------------------------------------------------------------------
path_figures = '../figures/'
fname = f'Voltage in time Amp:{amp} gex:{gex}'.replace(' ','_')
plt.savefig(path_figures + fname + '.png')