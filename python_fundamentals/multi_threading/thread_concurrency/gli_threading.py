'''
GLI - The Global Interpreter Lock (GIL) in Python is a mutex that ensures only one thread can execute Python bytecode at a time within a single Python process.

'''

import threading
import time

def brew_chai():
    print(f"Started {threading.current_thread().name } brewing...")

    count = 0
    for _ in range(100_000_000):
        count+=1

    print(f"Ended {threading.current_thread().name } brewing...")

t1 = threading.Thread(target=brew_chai, name="Barista-1")
t2 = threading.Thread(target=brew_chai, name="Barista-2")

start = time.time()
t1.start()
t2.start()

t1.join()
t2.join()

end = time.time()

print(f"Time taken to execute {end - start}")
