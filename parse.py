import sys
import h5py

filename = sys.argv[-1]
try:
    f = h5py.File(filename, 'r')
except:
    print("there is no such file")
    exit()
# List all groups
datasetNames = [n for n in f.keys()]
for n in datasetNames:
	print(n)

# Get the data
global_tallies = f['global_tallies']
global_tallies_data = global_tallies[:]
print(global_tallies_data)