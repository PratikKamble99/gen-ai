import threading
# import time
# def take_orders():
#     for i in range(4):
#         print(f"Taking Order from #{i+1}")
#         time.sleep(2)

# def brew_chai():
#     for i in range(4):
#         print(f"Brewing chai for #{i+1}")
#         time.sleep(4)

# # Create thread
# order_thread = threading.Thread(target=take_orders)
# brew_thread = threading.Thread(target=brew_chai)

# order_thread.start()
# brew_thread.start()

# brew_thread.join()
# order_thread.join()
# # wait for both to finish

# print(f"All orders taken and chai")


from pathlib import Path

BASE_DIR = Path(__file__).parent

def read_file(filename, label):
    with open(BASE_DIR / filename, "r") as file:
        for line in file:
            print(f"{label}--- {line.strip()}")

t1 = threading.Thread(target=read_file, args=("20mb.txt", "20MB"))
t2 = threading.Thread(target=read_file, args=("10mb.txt", "10MB"))

t2.start()
t1.start()
t2.join()
t1.join()
