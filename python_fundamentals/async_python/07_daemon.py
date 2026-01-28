import threading
import time

# A daemon thread runs in the background and is automatically killed when the main program exits.

def background_task():
    while True:
        print("Running in background...")
        time.sleep(1)

t = threading.Thread(target=background_task, daemon=True)
t.start()

time.sleep(3)
print("Main thread exiting")