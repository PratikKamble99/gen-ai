import asyncio

async def brew(name):
    print(f"Brewing Chai {name}")
    await asyncio.sleep(2) # THIS DOES NOT BLOCK NEXT TASK EXECUTION - Non blocking
    # time.time(2) # This is blocking
    print(f"Chai is ready: {name}")

async def main():
    await asyncio.gather(
        brew("Masala"),
        brew("Normal"),
        brew("special"),
    )

asyncio.run(main())