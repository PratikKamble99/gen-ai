import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

def encrypt(data):
    return f"🔒 {data[::-1]}"

async def main():
    # Gets the current running event loop
    loop = asyncio.get_running_loop()

    # Creates a pool of worker threads
    with ProcessPoolExecutor() as pool:
        # Offloading work to a thread
        result = await loop.run_in_executor(pool, encrypt, "credit_card_1234")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())