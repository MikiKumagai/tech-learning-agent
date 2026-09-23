"""MikiKumagai の全公開リポジトリ取得を確認するクライアント。"""

import sys
from pathlib import Path

import anyio
from mcp import Client, StdioServerParameters


async def main() -> None:
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve().with_name("server.py"))],
    )
    async with Client(server) as client:
        result = await client.call_tool(
            "list_github_repos",
            {
                "owner": "MikiKumagai",
            },
        )
        print(result)


if __name__ == "__main__":
    anyio.run(main)
