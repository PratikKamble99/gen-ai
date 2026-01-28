import threading

counter = 0
lock = threading.Lock()

def increment(thread_id):
    # print(f"Started in Thread {thread_id}")
    global counter # Making global memory I am making sure thread is getting shared memory not isolate
    for _ in range(100000):
        with lock: # making sure only one thread can modify counter
            print(f"Thread {threading.current_thread().name}")
            counter+=1

threads = [threading.Thread(target=increment, args=(i+1,)) for i in range(10)]

[t.start() for t in threads]
[t.join() for t in threads]

print(f"Final count {counter}")