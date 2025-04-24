import asyncio

async def fetch_data(delay: int) -> str:
    print("Getting data...")

    await asyncio.sleep(delay)
    print("Data received!")
    return f"Data after {delay} seconds"

async def main() -> None:
    print("learned about await keyword!")
    data = fetch_data(2)
    print("fetch_data function is called")

    real_data = await data
    print(real_data)
    print("fetch_data function is awaited")
    # loop = asyncio.get_event_loop()
    # data = loop.run_until_complete(fetch_data(2))
    # print(data)

if __name__ == "__main__":
    asyncio.run(main())
    # print(f"Main Function coroutine object: {main()}")
    #
    # print(f"fetch_data Function coroutine object: {fetch_data(5)}")