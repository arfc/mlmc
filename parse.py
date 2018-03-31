import sys
import csv
import h5py

filename = sys.argv[-1]
try:
    f = h5py.File(filename, 'r')
except:
    print("there is no such file")
    exit()
# List all groups
key_list = []
datasetNames = [n for n in f.keys()]
for n in datasetNames:
	key_list.append(n)

print(key_list)


import csv
point_state_csv =open("point_state.csv","w")
writer = csv.writer(point_state_csv)
writer.writerow(key_list)





# Get the data

for i in range(len(key_list)):
	result = []
	result.append(key_list[i]);
	temp = f[key_list[i]]
	print("temp is ", temp)
	temp_data = temp[:]
	for data in temp_data:
		result.append(data)
	writer.writerow(result)


global_tallies = f['global_tallies']
global_tallies_data = global_tallies[:]
print(global_tallies_data)