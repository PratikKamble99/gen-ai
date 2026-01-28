import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def check_stock(item):
    print(f"Checking {item} in store...")
    time.sleep(2)
    return f"{item} in stock: 42"

async def main():
    # Gets the current running event loop
    loop = asyncio.get_running_loop()

    # Creates a pool of worker threads
    with ThreadPoolExecutor() as pool:
        # Offloading work to a thread
        result = await loop.run_in_executor(pool, check_stock, "Masala Chai")
        print(result)

    """ 
        1.What happens internally:
        2.Event loop stays free
        3.check_stock() runs in a separate thread
        4.await pauses coroutine without blocking
        5.When thread finishes → result is returned
    """
    
asyncio.run(main())