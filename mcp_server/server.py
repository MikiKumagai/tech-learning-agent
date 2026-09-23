"""GitHub の公開リポジトリ情報を提供する MCP サーバー。"""

import json
import urllib.parse
import urllib.request
from typing import Any

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("tech-learning-server")


def _request_github(url: str) -> Any:
    """GitHub API の JSON を取得する。失敗時はエラーを呼び出し元へ返す。"""
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "tech-learning-agent",
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def _summarize_repo(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": data["name"],
        "full_name": data["full_name"],
        "description": data["description"],
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "url": data["html_url"],
    }


@mcp.tool()
def get_github_repo(owner: str, repo: str) -> dict[str, Any]:
    """GitHub の指定した公開リポジトリ情報を取得する。"""
    owner = urllib.parse.quote(owner, safe="")
    repo = urllib.parse.quote(repo, safe="")
    return _summarize_repo(_request_github(f"https://api.github.com/repos/{owner}/{repo}"))


@mcp.tool()
def list_github_repos(owner: str = "MikiKumagai") -> list[dict[str, Any]]:
    """指定ユーザーが所有する公開リポジトリを全件取得する。

    既定の対象は MikiKumagai。フォーク・アーカイブ済みも含めて全ページを取得する。
    返すのは名前・説明・主な言語・スター数・フォーク数・URL で、コード本文は含まない。
    """
    owner = urllib.parse.quote(owner, safe="")
    repositories = []
    page = 1
    per_page = 100

    while True:
        query = urllib.parse.urlencode({
            "type": "owner",
            "sort": "full_name",
            "direction": "asc",
            "per_page": per_page,
            "page": page,
        })
        data = _request_github(f"https://api.github.com/users/{owner}/repos?{query}")
        repositories.extend(_summarize_repo(repo) for repo in data)
        if len(data) < per_page:
            return repositories
        page += 1


if __name__ == "__main__":
    mcp.run()
