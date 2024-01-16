"""
cfg.py 

Simulation configuration for ...
This file has sim configs as well as specification for parameterized values in netParams.py 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""


import os
import numpy as np
from matplotlib import pyplot as plt
from netpyne import specs

cfg = specs.SimConfig()   


#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

cfg.coreneuron = False

rootFolder = os.getcwd()

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 25000.0 ## Duration of the sim, in ms  
cfg.dt = 0.05
# cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -65}  
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True
cfg.cvode_active = False
cfg.cvode_atol = 1e-6#1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.5

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True
cfg.checkErrors = False

cfg.allpops = []
cfg.allcells = ['sPY']

#------------------------------------------------------------------------------
# Net
#------------------------------------------------------------------------------

cfg.cellNumber = 256
# cfg.neuronsPerCore = 8
cfg.coresPerNode = 16 # int(np.ceil(cfg.cellNumber / cfg.neuronsPerCore))
cfg.neuronsPerCore = cfg.cellNumber / cfg.coresPerNode

cfg.gex = 0.000111 # default 0.0005
cfg.n_neighbors = 30 #int(0.3 * cfg.cellNumber) # all conetions 
cfg.amp = 0.170
cfg.synapse_delay = cfg.dt + 1e-5 #0.05 #1 #0.01

for cell in cfg.allcells:
    cfg.allpops.append(f'pop_{cell}')

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
# cfg.analysis['plotTraces'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'oneFigPer':'trace', 'axis': False, 'subtitles':False,'timeRange': [cfg.duration-5000,cfg.duration], 'legend':False, 'overlay':False, 'figSize':(36, 24), 'fontSize':2}
cfg.analysis['plotRaster'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'popRates': False, 'orderInverse': True, 'timeRange': [cfg.duration-2000,cfg.duration],'figSize': (10,4), 'lw': 0.3, 'markerSize':10, 'marker': '.', 'dpi': 200}
# cfg.analysis['plot2Dnet']   = {
#     'include': cfg.allpops , 'saveFig': True, 'showFig': False, 'showConns': True,
#     'figSize': (12,12), 'view': 'xz', 'fontSize':12,
#     }

#------------------------------------------------------------------------------
# Current inputs  
#------------------------------------------------------------------------------
cfg.addIClamp = 1
delaystim = 0
cfg.IClamp0 =   {
    'pop': cfg.allpops[0],
    'sec': 'soma',
    'loc': 0.5,
    'start': delaystim,
    'dur': cfg.duration,
    'amp': cfg.amp #0.0175
    }    

# spikes during 50 ms to create desyncronization
cfg.desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
cfg.desyncr_spikes_dur = 500 # defaut 500 = 50 ms
cfg.numCellsDesync = 70 #100 # numCells to produce desyncronization
cfg.percentConsDesync = 0.1

#------------------------------------------------------------------------------
# Record Data 
#------------------------------------------------------------------------------

# cfg.recordCells = cfg.allpops  # which cells to record from
# cfg.recordTraces = {'V_soma': {'sec':'soma_0', 'loc':0.5, 'var':'v'}}  ## Dict with traces to record
# cfg.recordStim = True
# cfg.recordTime = True
cfg.recordStep = 0.05            

cfg.simLabel = 'v0_batch0'
cfg.saveFolder = '../data/'+cfg.simLabel
# cfg.filename =                	## Set file output name
cfg.savePickle = True         	## Save pkl file
cfg.saveJson = False           	## Save json file
cfg.saveDataInclude = ['simConfig', 'netParams', 'simData', 'net'] ## 
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = False			##  
cfg.saveCellConns = False		##