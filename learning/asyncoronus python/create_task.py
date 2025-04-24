import asyncio
import time
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
    return f"Task {id_number}: Data received after {delay} seconds"

async def main() -> None:
    """
    Main function to run the async tasks
    :return:
    """
    print("learned about create_task() function!")
    task_1 = asyncio.create_task(fetch_data(1, 2))
    task_2 = asyncio.create_task(fetch_data(2, 3))
    task_3 = asyncio.create_task(fetch_data(3, 1))

    # Run the tasks one by one
    result_1 = await task_1
    print(result_1)
    result_2 = await task_2
    print(result_2)
    result_3 = await task_3
    print(result_3)

if __name__ == "__main__":
    asyncio.run(main())


