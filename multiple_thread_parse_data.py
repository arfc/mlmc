# import thread
import threading
import sys

try:
    # batch_number = int(sys.argv[-4])
    # generation_number = int(sys.argv[-3])
    # particle_number = int(sys.argv[-2])
    # csv_name = sys.argv[-1]
    batch_number = int(10)
    generation_number = int(10)
    particle_number = int(10)
except:
    print(
        "There should be four arguments standing for batch number,generation number,particle number,csv name repectively")
    exit()

# list of all file names
filename_list = []

def append_next_file_name():
    global filename_list
    global batch_number
    global particle_number
    global generation_number
    if len(filename_list) == 0:
        filename_list.append([1, 1, 1])
        return True
    temp = filename_list[-1]
    next_particle_number = temp[2]
    next_generatipn_number = temp[1]
    next_batch_number = temp[0]

    if temp[2] < particle_number:
        next_particle_number = temp[2] + 1
        filename_list.append([next_batch_number,next_generatipn_number,next_particle_number])
        return True
    elif generation_number & temp[0] < batch_number & temp[0] < batch_number:
        next_particle_number = 1
    if temp[1] < generation_number:
        next_generatipn_number = temp[1] + 1
        filename_list.append([next_batch_number,next_generatipn_number,next_particle_number])
        return True
    elif temp[0] < batch_number:
        next_generatipn_number = 1
    if temp[0] < batch_number:
        next_batch_number = temp[0] + 1
        filename_list.append([next_batch_number,next_generatipn_number,next_particle_number])

    else:
        print("that's all")
        return False


class getThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global filename_list
        print("Starting " + self.name)
        while(1):
            threadLock.acquire()
            result = append_next_file_name()
            threadLock.release()
            if result is False:
                break


threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = getThread(1, "Thread-1", 1)
thread2 = getThread(2, "Thread-2", 2)
thread3 = getThread(3, "Thread-2", 3)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

# 等待所有线程完成
for t in threads:
    t.join()
print("hahah")
print(filename_list)
print(len(filename_list))
