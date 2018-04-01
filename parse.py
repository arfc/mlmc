import sys
import csv
import h5py

csv_name = sys.argv[-1]
filename = sys.argv[-2]
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

point_state_csv =open(csv_name,"w")
writer = csv.writer(point_state_csv)
writer.writerow(key_list)

# Get the data
# print(key_list)
for i in range(len(key_list)):
	result = []
	result.append(key_list[i]);

	temp = f[key_list[i]]
	try:
		temp_data = temp[:]
		for data in temp_data:
			result.append(data)
			# print("wocao shape is ",data.shape)
			# print("wocao data is ",data)
		writer.writerow(result)
	except:
		print(key_list[i]," is empty")

# global_tallies = f['global_tallies']
# global_tallies_data = global_tallies[:]
# print(global_tallies_data)



