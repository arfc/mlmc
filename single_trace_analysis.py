import h5py
import csv
import sys

batch_number = sys.argv[-3]
generation_number = sys.argv[-2]
particle_number = sys.argv[-1]

filename = str("track_"+batch_number+"_"+generation_number+"_"+particle_number+".h5")
print(filename)

try:
    f = h5py.File(filename, 'r')
except:
    print("there is no such file")
    exit()
