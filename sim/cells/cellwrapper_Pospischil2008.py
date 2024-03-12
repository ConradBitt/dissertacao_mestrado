import os
from neuron import h # NEURON simulator

def loadCell(template):
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    h.xopen(f'cells/{template}_template')
    print ("Loading cell", template)
    cell = getattr(h, template)(0)
    print (f'Creating a generic {template} cell from Pospischil2008 template')
    return cell
    
