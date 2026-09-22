"""GitHub リポジトリ取得ツールの動作確認用クライアント。"""

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
            "get_github_repo",
            {
                "owner": "MikiKumagai",
                "repo": "progress_management",
            },
        )
        print(result)


if __name__ == "__main__":
    anyio.run(main)
