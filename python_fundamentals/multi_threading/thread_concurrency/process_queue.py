from multiprocessing import Process, Queue
import time

def prepare_chai(queue):
    queue.put("Masala Chai is ready")

if __name__ == "__main__":
    start = time.time()
    queue = Queue()

    processes = [Process(target=prepare_chai, args=(queue, )) for _ in range(2)]

    [p.start() for p in processes]
    [p.join() for p in processes]

    print(queue.get())

