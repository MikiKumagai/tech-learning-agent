"""GitHub の公開リポジトリ情報を提供する MCP サーバー。"""

import json
import urllib.request
from typing import Any

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("tech-learning-server")


@mcp.tool()
def get_github_repo(owner: str, repo: str) -> dict[str, Any]:
    """GitHubの公開リポジトリ情報を取得する。"""

    url = f"https://api.github.com/repos/{owner}/{repo}"

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "tech-learning-agent",
        },
    )

    with urllib.request.urlopen(request) as response:
        data = json.load(response)

    return {
        "name": data["name"],
        "full_name": data["full_name"],
        "description": data["description"],
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "url": data["html_url"],
    }


if __name__ == "__main__":
    mcp.run()
