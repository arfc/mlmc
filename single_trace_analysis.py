import h5py
import csv
import sys


#get the batch number,generation number,particle number from the arguments
try:
	batch_number = sys.argv[-4]
	generation_number = sys.argv[-3]
	particle_number = sys.argv[-2]
	csv_name = sys.argv[-1]
except:
    print("There should be four arguments standing for batch number,generation number,particle number,csv name repectively")
    exit()
#get all the file names as a list
file_name_list = []

for i in range(int(batch_number)):
	for j in range(int(generation_number)):
		for k in range(int(particle_number)):
			temp_name = str("track_"+i+"_"+j+"_"+k+".h5")
			file_name_list.append(temp_name)
#total particles
total = i*j*k

point_state_csv =open(csv_name,"w")
writer = csv.writer()
writer.writerow(key_list)  

# for filename in file_name_list:
def get_single_track(filename):
	print("wocao")
	try:
		f = h5py.File(filename, 'r')
	except:
		print("there is no such file")
		exit()

	key_list = []
	datasetNames = [n for n in f.keys()]

	for n in datasetNames:
		key_list.append(n)

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

for filename in file_name_list:
	get_single_track(filename)

# Get the data
# print(key_list)

