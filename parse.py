import sys
import h5py

filename = sys.argv[-1]
try:
    f = h5py.File(filename, 'r+')
except:
    print("there is no such file")
    exit()
# List all groups
print("Keys: %s" % f.keys())
#a_group_key = list(f.keys())[0]

# Get the data
#data = list(f[a_group_key])


#print(data)

