import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import unicodedata
from copy import deepcopy
import re


# space
# velocity = 
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

# def spilt_space(senternce_data):
# 	space = []
# 	cur = 0
# 	count = 0
# 	while(i<len(senternce_data)):
# 		if 
def form_sentence_data(sentence_data):
	# result = sentence_data.split(',')
	# for data in result:
	# 	# print(type(data))
	# 	print(data)
	# 	print(re.sub('-{1,2}', '', 'pro----gram-files'))

	# 	print("dealt data",line)
	for char in '[]() ':
		sentence_data = re.sub('\\'+char,'',sentence_data)
	data_list = sentence_data.split(',')
	# print(data_list)
	result = np.zeros(len(data_list))
	# print("len is ", len(sentence_data))
	for index in range(len(data_list)):
		result[index] = float(data_list[index])
		# print(float(data_list[index]))
		# result[index]+= result[index]

	# print(result)
	# # result = re.sub('\[','', sentence_data)
	# # result = re.sub('\]','', result)
	# # sentence_data = re.sub('[]','', sentence_data)
	# # sentence_data = re.sub(' ','', sentence_data)
	# # print(re.sub('\(','', 'pro----,[gram]-files'))
	return result


space = []
velocity = []
group = []
c=open("point_state.csv","r") #以rb的方式打开csv文件
read=csv.reader(c)
for line in read:
	if(line[0] == 'source_bank'):
		# print("wocaonima")
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

space_x = np.zeros(len(space))
space_y = np.zeros(len(space))
space_z = np.zeros(len(space))

for i in range(len(space)):
	space_x[i] = space[i][0]
	space_y[i] = space[i][1]
	space_z[i] = space[i][2]


# print(space_[0])
# print(velocity[0])
# print(group)


# def randrange(n, vmin, vmax):
#  '''
#  Helper function to make an array of random numbers having shape (n, )
#  with each number distributed Uniform(vmin, vmax).
#  '''
#  return (vmax - vmin)*np.random.rand(n) + vmin
 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
 
# n = 100
 
# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#  xs = randrange(n, 23, 32)
#  ys = randrange(n, 0, 100)
#  zs = randrange(n, zlow, zhigh)
ax.scatter(space_x, space_y, space_z, c='r', marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
 
plt.show()

