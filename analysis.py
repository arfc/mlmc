import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import unicodedata
from copy import deepcopy
import re

from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
 
def form_sentence_data(sentence_data):
	# result = sentence_data.split(',')
	for char in '[]() ':
		sentence_data = re.sub('\\'+char,'',sentence_data)
	data_list = sentence_data.split(',')
	# print(data_list)
	result = np.zeros(len(data_list))
	# print("len is ", len(sentence_data))
	for index in range(len(data_list)):
		result[index] = float(data_list[index])

	return result

def form_sentence_data_np(sentence_data):
	# result = sentence_data.split(',')
	for char in '[]':
		sentence_data = re.sub('\\'+char,'',sentence_data)
	data_list = sentence_data.split(' ')
	try:
		while(1):
			data_list.remove('')
	except:
		print("finish")
	result = np.zeros(len(data_list))
	# print("len is ", len(sentence_data))
	for index in range(len(data_list)):
		result[index] = float(data_list[index])

	return result

space = []
velocity = []
group = []
c=open("point_state.csv","r") #以rb的方式打开csv文件
read=csv.reader(c)
for line in read:
	if(line[0] == 'source_bank'):
		for index in range(1,len(line)):

			data_list = form_sentence_data(line[index])
			temp_space = []
			for i in range(1,4):
				temp_space.append(data_list[i])
			space.append(temp_space)
			temp_velocity = []
			for i in range(4,7):
				temp_velocity.append(data_list[i])
			velocity.append(temp_velocity)
			group.append(data_list[len(data_list)-1])
	  # for i in range(1,len(line)):
	  # 	print(line[i])
c.close()


final = []

with open("test.csv","r") as track:
	reader = csv.reader(track)
	for line in reader:
		data_list = form_sentence_data_np(line[len(line)-1])
		final.append(data_list)

final = np.array(final)

single_track = []
with open("test.csv","r") as track:
	reader = csv.reader(track)
	for line in reader:
		print(len(line))
		for data in line:
			try:
				data_list = form_sentence_data_np(data)
				single_track.append(data_list)
			except:
				print("head data")
		break

single_track = np.array(single_track)
print(single_track)



# space_x = np.zeros(len(space))
# space_y = np.zeros(len(space))
# space_z = np.zeros(len(space))

# for i in range(len(space)):
# 	space_x[i] = space[i][0]
# 	space_y[i] = space[i][1]
# 	space_z[i] = space[i][2]

# print(len(space))
# np_space = np.array(space)
# meandistortions = []
# K = range(1, 10)
# for k in K:
#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(np_space)
#     meandistortions.append(sum(np.min(cdist(np_space, kmeans.cluster_centers_, 'euclidean'), axis=1)) / np_space.shape[0])

# plt.figure()
# plt.grid(True)
# plt1 = plt.subplot(2,1,1)
# plt1.plot(np_space[:,0],np_space[:,1],'k.');
# plt2 = plt.subplot(2,1,2)
# plt2.plot(K, meandistortions, 'bx-')
# plt.show()
space = np.array(space)
# # print(space[:,0])

fig = plt.figure(12)
source_bank = fig.add_subplot(331, projection='3d')
 
source_bank.scatter(space[:,0], space[:,1], space[:,2], c='r', marker='.')
source_bank.set_xlabel('X Label')
source_bank.set_ylabel('Y Label')
source_bank.set_zlabel('Z Label')

final_track = fig.add_subplot(332, projection='3d')
 
final_track.scatter(final[:,0], final[:,1], final[:,2], c='b', marker='.')
final_track.set_xlabel('X Label')
final_track.set_ylabel('Y Label')
final_track.set_zlabel('Z Label')

final_xy = fig.add_subplot(334)
final_xy.scatter(final[:,0], final[:,1], c='b', marker='.')
final_xy.set_xlabel('X')
final_xy.set_ylabel('Y')


final_yz = fig.add_subplot(335)
final_yz.scatter(final[:,1], final[:,2], c='y', marker='.')
final_yz.set_xlabel('Y')
final_yz.set_ylabel('Z')
# final_yz.title("yz plain")

final_xz = fig.add_subplot(336)
final_xz.scatter(final[:,1], final[:,2], c='g', marker='.')
final_xz.set_xlabel('Y')
final_xz.set_ylabel('Z')
print("len is ", len(single_track))
ax = fig.gca(projection='3d')
sample_track = ax.plot(single_track[:,0], single_track[:,1],single_track[:,2], c='r', marker='.')
# sample_track.set_xlabel('Y')
# sample_track.set_ylabel('Z')
# sample_track.set_zlabel('Z')
# final_xz.title("xz plain")
plt.show()

