import anyio

from mcp import Client, StdioServerParameters


server = StdioServerParameters(
    command="python",
    args=["mcp_server/server.py"],
)


async def main():
    async with Client(server) as client:
        result = await client.call_tool(
            "get_learning_topics",
            {},
        )

        print(result)


if __name__ == "__main__":
    anyio.run(main)