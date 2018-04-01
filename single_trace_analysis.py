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

key_list = []
datasetNames = [n for n in f.keys()]
for n in datasetNames:
	key_list.append(n)

print(key_list)

# point_state_csv =open(csv_name,"w")
# writer = csv.writer(point_state_csv)
# writer.writerow(key_list)

# # Get the data
# # print(key_list)
# for i in range(len(key_list)):
# 	result = []
# 	result.append(key_list[i]);

# 	temp = f[key_list[i]]
# 	try:
# 		temp_data = temp[:]
# 		for data in temp_data:
# 			result.append(data)
# 			# print("wocao shape is ",data.shape)
# 			# print("wocao data is ",data)
# 		writer.writerow(result)
# 	except:
# 		print(key_list[i]," is empty")
