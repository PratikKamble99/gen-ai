from multiprocessing import Process
import time

def crunch_number():
    print(f"Started the count process...")
    count = 0
    for _ in range(100_000_000):
        count+=1
    print(f"Ended the count process...")

# start = time.time()

# p1 = Process(target=crunch_number)
# p2 = Process(target=crunch_number)

# p1.start()
# p2.start()

# p1.join()
# p2.join()

# end = time.time()

# print(f"Time taken {start-end}")

'''
    When you call processes without checking if main process is there then python not found which process is entry point and throws error
    SO always check if main thread is and then run processes
'''

if __name__ == "__main__":
    start = time.time()

    p1 = Process(target=crunch_number)
    p2 = Process(target=crunch_number)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end = time.time()

    print(f"Time taken {end-start}")