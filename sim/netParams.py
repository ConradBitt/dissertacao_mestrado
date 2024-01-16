
"""
netParams.py

... model using NetPyNE

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import os
import numpy as np

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = 1.0 # Scale factor for number of cells
netParams.sizeX = 100.0 # x-dimension (horizontal length) size in um
netParams.sizeY = 100.0 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100.0 # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume
   
netParams.propVelocity = 300.0    # propagation velocity (um/ms)
netParams.probLengthConst = 10.0 # length constant for conn probability (um)


#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
for cellName in cfg.allcells:
    cellRule = netParams.importCellParams(label=cellName + '_rule', somaAtOrigin=False,
        conds={'cellType': cellName, 'cellModel': 'HH_simple'},
        fileName='cells/PospischilEtAl2008/cellwrapper_Pospischil2008.py',
        cellName='loadCell',
        cellArgs={'template': cellName},
        cellInstance = True,
        importSynMechs=True
        )

    # observation:
    # - when import template cells the label of 'soma' is 'soma_0'.
    print(netParams.cellParams[cellName + '_rule']['secs']['soma_0'])

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

# for ith-pop create pop with ith-cell of allcells 

for i, pop in enumerate(cfg.allpops):
    netParams.popParams[pop] = {
        'cellType': cfg.allcells[i],
        'cellModel': 'HH_simple',
        'numCells': cfg.cellNumber
    }

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
     for key in [k for k in dir(cfg) if k.startswith('IClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # add stim source
        netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': f'{sec}_0', # target 'soma_0'
            'loc': loc}


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------

# netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 15.0, 'tau2': 150.0, 'e': 0.0}
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0.0}
#ESynMech    = ['AMPA', 'NMDA']
#------------------------------------------------------------------------------
# Connectivity rules
#------------------------------------------------------------------------------
## Spatial disposition of neurons
r = netParams.sizeX/2.0  # radius of circle
dist_between_neurons = 2.0*r*np.sin(np.pi/cfg.cellNumber)
radius_conns = cfg.n_neighbors * dist_between_neurons + 0.001

prob = '(dist_2D<%s)' % (radius_conns)

# print(dist_between_neurons,radius_conns,prob)
netParams.connParams['EE'] = { 
    'preConds': {'pop': cfg.allpops},
    'postConds': {'pop': cfg.allpops},
    'synMech': 'AMPA', 
    'probability': prob, 
    'delay' : cfg.synapse_delay, # If omitted, defaults to netParams.defaultDelay = 1ms
    'weight': cfg.gex,
    }

# connect initial spikes
netParams.connParams['initialrandom'] = { 
    'preConds': {'pop': 'initialspikes'},
    'postConds': {'pop': cfg.allpops},
    'synMech': 'AMPA', # target synaptic mechanism
    'probability': 0.5, # 1., 
    'weight': 0.0001, 
    'delay': cfg.synapse_delay
    }  


#------------------------------------------------------------------------------
# Description
#------------------------------------------------------------------------------
netParams.description = f"""
- v1    ** Locking for a chimera states in to frequency range (max 20hz)
        - Network with 200 neurons, duration 20000ms
        - cellNumber: 200
        - gex: [np.round(1e-5*vv, 6) for vv in range(2,66,4)]
        - n_neighbors: [vv for vv in range(2,66,4)]
        - amp: 170pA
        - synapse_delay: 0.05
        - cores per node 80

- v2    ** Locking for a chimera states in to frequency range (max 200hz)
        - Network with 128 neurons, duration 25000ms
        - amp: 170pA
        - synapse_delay: 0.05
        - n = cfg.cellNumber # = 128
        - resol = 16
        - gex = [round(1e-5*vv, 6) for vv in np.linspace(10,50,resol)]
        - p = np.linspace((resol/(4*n)), 0.400, resol)
        - n_cons_network = (n * p).astype(int)
        - ncons = np.array_split(n_cons_network, 2)
        - nodes = 8
        - 8 neurons per core
        - cores per node 16

- v3    ** Locking for a chimera states in to frequency range (max 200hz)
        - Network with 256 neurons, duration 25000ms
        - amp: 170pA
        - synapse_delay: 0.05
        - n = cfg.cellNumber # = 256
        - resol = 32
        - gex = [round(1e-5*vv, 6) for vv in np.linspace(10,50,resol)]
        - p = np.linspace((resol/(4*n)), 0.400, resol)
        - n_cons_network = (n * p).astype(int)
        - ncons = np.array_split(n_cons_network, 2)
        - nodes = 16
        - 8 neurons per core
        - cores per node 32


- v4    ** Locking for a chimera states in to frequency range (max 200hz)
        - Network with 256 neurons, duration 25000ms
        - amp: np.linspace(0.14, 0.3, 32),4
        - synapse_delay: 0.05
        - n = cfg.cellNumber # = 256
        - n = cfg.n_neighbors = 52
        - resol = 32
        - gex = [round(1e-5*vv, 6) for vv in np.linspace(10, 45, 32)]
        - nodes = 16
        - 8 neurons per core
        - cores per node 32

- v4    ** Locking for a chimera states in to frequency range (max 200hz)
        - Network with 256 neurons, duration 25000ms
        - amp: np.linspace(0.14, 0.3, 32),4
        - neighbours = np.arange(2,66,2)
        - synapse_delay: 0.05
        - n = cfg.cellNumber # = 256
        - resol = 32
        - cfg.gex = 0.00025
        - nodes = 16
        - 8 neurons per core
        - cores per node 32

- v5    ** Locking for a chimera states in to frequency range (max 200hz)
        - Network with 256 neurons, duration 25000ms
        - amp: np.linspace(0.14, 0.3, 32),4
        - neighbours = np.arange(2,66,2)
        - synapse_delay: 0.05
        - n = cfg.cellNumber # = 256
        - resol = 32
        - cfg.gex = 0.00025
        - nodes = 16
        - 8 neurons per core
        - cores per node 32
"""