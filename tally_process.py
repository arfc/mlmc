import openmc
import numpy as np

sp = openmc.StatePoint('statepoint.100.h5')
detector_data = sp.get_tally(name='detector')

print(detector_data)