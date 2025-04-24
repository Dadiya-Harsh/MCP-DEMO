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

    print("learned about TaskGroup function!")

    tasks = []

    """
    Create a TaskGroup to manage multiple tasks and,
    we are using async with statement which is used to create a context manager for the TaskGroup.
    This ensures that all tasks are completed before exiting the context.
    """
    async with asyncio.TaskGroup() as tg:
        for i, sleep_time in enumerate([2, 3, 4], start=1):
            tasks.append(tg.create_task(fetch_data(i, sleep_time)))

    results = [task.result() for task in tasks]


    for results in results:
        print(f"Received results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
    # print(f"Main Function coroutine object: {main()}")
    #
    # print(f"fetch_data Function coroutine object: {fetch_data(5)}")