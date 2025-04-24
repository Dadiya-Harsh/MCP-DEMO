import asyncio

async def fetch_data(id_number: int, delay: int) -> str:
    """
    Simulate a network call to fetch data
    :param:
        id_number: id of the task
        delay: time to wait before returning data
    :return:
        string that contains how much time it took to fetch data
    """

    print(f"Task {id_number}: Getting data...")
    await asyncio.sleep(delay)
    print(f"Task {id_number}: Data received!")
    return f"Task {id_number}: Data after {delay} seconds"

async def main() -> None:
    """
    Main function to run the async tasks
    :return:
    """

    print("learned about await keyword!")

    # Create a list of tasks
    tasks = [
        fetch_data(1, 2),
        fetch_data(2, 3),
        fetch_data(3, 1)
    ]

    # Run the tasks concurrently
    results = await asyncio.gather(*tasks)
    """
    Note:
        if we are using asyncio.gather(), we should remember it is not good at error handling, so use it carefully.
        If one of the tasks or coroutine fails, it will not cancel other tasks or coroutine.
    """

    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())