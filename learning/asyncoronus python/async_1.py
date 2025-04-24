import asyncio

async def main() -> None:
    """
    whenever async function is called, it returns a coroutine object
    :return:
    """

    print("Hello from mcp-demo!")

if __name__ == "__main__":
    asyncio.run(main())