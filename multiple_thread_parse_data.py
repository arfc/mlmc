# import thread
import threading
import sys
import h5py
import numpy as np
import sklearn
import csv
try:
    batch_number = int(sys.argv[-4])
    generation_number = int(sys.argv[-3])
    particle_number = int(sys.argv[-2])
    csv_name = sys.argv[-1]
    # batch_number = int(10)
    # generation_number = int(1)
    # particle_number = int(10)
except:
    print(
        "There should be four arguments standing for batch number,generation number,particle number,csv name repectively")
    exit()

# list of all file names
filename_list = []
final_states = []
def append_next_file_name():
    global filename_list
    global batch_number
    global particle_number
    global generation_number
    if len(filename_list) == 0:
        filename_list.append([1, 1, 1])
        return [1,1,1]
    temp = filename_list[-1]
    next_particle_number = temp[2]
    next_generation_number = temp[1]
    next_batch_number = temp[0]

    if temp[2] < particle_number:
        next_particle_number = temp[2] + 1
        result = [next_batch_number, next_generation_number, next_particle_number]
        filename_list.append(
            result)
        return result

    elif temp[1] < generation_number or temp[0] < batch_number:
        next_particle_number = 1

    if temp[1] < generation_number:
        next_generation_number = temp[1] + 1
        result = [next_batch_number, next_generation_number, next_particle_number]
        filename_list.append(result)
        return result

    elif temp[0] < batch_number:
        next_generation_number = 1

    if temp[0] < batch_number:
        next_batch_number = temp[0] + 1
        result = [next_batch_number, next_generation_number, next_particle_number]
        filename_list.append(result)
        return result

    else:
        print("that's all")
        return None

def get_file_name(number_array):
    result = "track_%d_%d_%d.h5" % (number_array[0],number_array[1],number_array[2])
    return result



def get_final_state(file_name):
    #print("try to get final state")
    print(file_name)
    try:
        f = h5py.File(file_name, 'r')
    except:
        print("there is no such file")
        exit()
    #print("has the file")
    datasetNames = [n for n in f.keys()]
    for key in datasetNames:
        temp = f[key]
        try:
            temp_data = temp[:]
            final_states.append(temp_data[-1])
        except:
            print("empty")



class getThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global filename_list
        print("Starting " + self.name)
        while (1):
            threadLock.acquire()
            result = append_next_file_name()
            threadLock.release()

            if result is None:
                break
            else:
                file_name = get_file_name(result)
                get_final_state(file_name)


threadLock = threading.Lock()

threads = []

# create threads
for i in range(1,5):
    temp_thread = getThread(i,"Thread-"+str(i),i)
    temp_thread.start()
    threads.append(temp_thread)
# wait join threads
for t in threads:
    t.join()

final_states = np.array(final_states)
final_states_csv =open(csv_name,"w")
writer = csv.writer(final_states_csv)
writer.writerow(final_states)
print(len(filename_list))
print(final_states)
print(type(final_states))
