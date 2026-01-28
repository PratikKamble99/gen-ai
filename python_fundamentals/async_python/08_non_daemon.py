import threading
import time

""" 
    👉 Program will NOT exit
    👉 Main thread waits until this thread finishes (or forever)
 """

def background_task():
    while True:
        print("Running in background...")
        time.sleep(1)

t = threading.Thread(target=background_task,)
t.start()

time.sleep(3)
print("Main thread exiting")