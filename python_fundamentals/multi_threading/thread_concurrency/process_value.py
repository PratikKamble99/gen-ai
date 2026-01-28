from multiprocessing import Process, Value
import time

def increment(counter):
    for _ in range(100000):
        with counter.get_lock():
            counter.value+=1


if __name__ == "__main__":
    start = time.time()
    counter = Value("i", 0)

    # this is how we share same memory with processes
    processes = [Process(target=increment, args=(counter, )) for _ in range(4)]

    [p.start() for p in processes]
    [p.join() for p in processes]

    print(f"Final counter value: ", counter.value)
