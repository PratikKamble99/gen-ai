import threading

lock_a = threading.Lock()
lock_b = threading.Lock()


""" 
    1️⃣ Thread t1 starts
    Task 1 acquired lock a
    t1 holds lock_a
    Tries to acquire lock_b → ❌ blocked

    2️⃣ Thread t2 starts
    Task 2 acquired lock b
    t2 holds lock_b
    Tries to acquire lock_a → ❌ blocked

    Final state ❌
    t1 holds lock_a, waiting for lock_b
    t2 holds lock_b, waiting for lock_a

    🔒 Circular wait → DEADLOCK
 """

def task_1():
    with lock_a:
        print("Task 1 acquired lock a")
        with lock_b:
            print("Task 1 acquired lock b")

def task_2():
    with lock_b:
        print("Task 2 acquired lock b")
        with lock_a:
            print("Task 2 acquired lock a")

t1 = threading.Thread(target=task_1)
t2 = threading.Thread(target=task_2)

t1.start()
t2.start()
