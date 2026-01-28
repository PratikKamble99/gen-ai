import asyncio

async def brew():
    print("Brewing Chai...")
    await asyncio.sleep(2)
    print("Chai is ready")

asyncio.run(brew())