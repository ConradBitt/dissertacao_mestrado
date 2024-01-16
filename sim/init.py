"""
init.py

Starting script to run NetPyNE-based model.

Usage:
    - First, in the "sim" folder, run "nrnivmodl mod" in the terminal.
    - then python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""
from netpyne import sim
import pickle, json
import numpy as np
import os
import datetime

inicio = datetime.datetime.now()
# cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
cfg, netParams = sim.readCmdLineArgs()

sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations

r = 50  # radius
center = (50, 50) # center in um
theta = np.linspace(0, 2*np.pi, cfg.cellNumber)  # angle 
x = center[0] + r*np.cos(theta) # x-values in um
z = center[1] + r*np.sin(theta) # z-values in um

print(20*'=--=')
print(10*' ' + f' Ajusting networt')
print(20*'----')

print("print(sim.rank,sim.nhosts, len(sim.net.cells), sim.net.cells[0].tags)")
print(sim.rank, sim.nhosts, len(sim.net.cells), sim.net.cells[0].tags)
for ii, metype in enumerate(sim.net.cells):
    ## ii ii is within range 0 to neuronsPerCore
    ## sim.rank have a neuronsPerCore structures 
    # verificar a estrutura da rede com e sem o código abaixo
    # i =  sim.rank * len(sim.net.cells) + ii # indice global do neuronio
    i =  sim.rank * len(sim.net.cells) + ii

    # looping to change the spatial coordinates of neurons
    metype.tags['x'] = x[i]     # x positions in um
    metype.tags['y'] = 50.0
    metype.tags['z'] = z[i]     # z positions in um
    metype.tags['xnorm'] = x[i]/100.0
    metype.tags['ynorm'] = 0.5
    metype.tags['znorm'] = z[i]/100.0


print(20*'----')
print(sim.rank, sim.nhosts, len(sim.net.cells), sim.net.cells[0].tags)
print(20*'----')


sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  
sim.gatherData()                  			# gather spiking data and cell info from each node
sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc

# sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_rate.json', stats=['rate'], saveFig=True)
# sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_CV.json', stats=['isicv'], saveFig=True)
# sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_sync.json', stats=['sync'], saveFig=True);


fim = datetime.datetime.now()

print(20*'=--=')
print(10*' ' + f'Total time running simulation: {fim - inicio}')
print(20*'----')