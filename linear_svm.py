import numpy as np
from sklearn import svm
from sklearn import preprocessing
from sklearn import utils

original_data_matrix = np.loadtxt("data_simulation.txt")
total_status = len(original_data_matrix)


def mapping(i):
    result = np.zeros(shape=6)

    return result


def status_matrix_transfer(origin, pos_flag):
    index = 0
    for i in range(total_status):
        if pos_flag:
            if origin[i][7] > 0.5:
                index += 1
        else:
            if origin[i][7] < 0.5:
                index += 1
    status_matrix = np.zeros(shape=(index, 6))
    index = 0
    for i in range(total_status):
        if pos_flag:
            if origin[i][7] < 0.5:
                continue
        else:
            if origin[i][7] > 0.5:
                continue
        status_matrix[index][0] = origin[i][0]
        status_matrix[index][1] = origin[i][3]
        status_matrix[index][2] = origin[i][1]
        status_matrix[index][3] = origin[i][4]
        status_matrix[index][4] = origin[i][2]
        status_matrix[index][5] = origin[i][5]
        # status_matrix[index][6] = origin[i][7]
        index += 1
    return status_matrix


def input_matrix_transfer(origin):
    status_matrix = np.zeros(shape=(total_status, 6))
    for i in range(total_status):
        status_matrix[i][0] = origin[i][0]
        status_matrix[i][1] = origin[i][3]
        status_matrix[i][2] = origin[i][1]
        status_matrix[i][3] = origin[i][4]
        status_matrix[i][4] = origin[i][2]
        status_matrix[i][5] = origin[i][5]
        # status_matrix[index][6] = origin[i][7]
    return status_matrix


def output_matrix_transfer(origin):
    status_matrix = np.zeros(shape=total_status)
    for i in range(total_status):
        status_matrix[i] = origin[i][7]
        # status_matrix[index][6] = origin[i][7]
    return status_matrix


pos = status_matrix_transfer(original_data_matrix, 1)
neg = status_matrix_transfer(original_data_matrix, 0)
X = input_matrix_transfer(original_data_matrix)
Y = output_matrix_transfer(original_data_matrix)

lab_enc = preprocessing.LabelEncoder()
encoded = lab_enc.fit_transform(Y)
clf = svm.SVC()
print("我日")
print(utils.multiclass.type_of_target(encoded))

clf.fit(X, encoded)
print("我日")
print(clf.predict([0.1, 0.2, 0.3, 0.4, 0.1, 0.2]))
