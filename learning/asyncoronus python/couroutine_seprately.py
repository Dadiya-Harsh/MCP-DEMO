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

    data_1 = fetch_data(1, 2)
    print(await data_1)
    print("fetch_data function is called for task 1")

    data_2 = fetch_data(2, 3)
    print(await data_2)
    print("fetch_data function is called for task 2")

    data_3 = fetch_data(3, 1)
    print(await data_3)
    print("fetch_data function is called for task 3")

    # Run the tasks concurrently
    # results = await asyncio.gather(*tasks)

    # for result in results:
    #     print(result)


if __name__ == "__main__":
    asyncio.run(main())
    # print(f"Main Function coroutine object: {main()}")
    #
    # print(f"fetch_data Function coroutine object: {fetch_data(5)}")