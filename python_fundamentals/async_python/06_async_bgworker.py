import threading
import time
import asyncio

def background_worker():
    while True:
        print(f"Logging system health ⏱️")
        time.sleep(1)

async def fetch_order():
    await asyncio.sleep(4)
    print(f"Order fetched 🎁")

threading.Thread(target=background_worker, daemon=True).start()

asyncio.run(fetch_order())