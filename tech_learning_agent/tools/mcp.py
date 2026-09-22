"""ローカル MCP サーバーと ADK の接続。"""

import sys

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from ..config import MCP_SERVER_PATH


def create_mcp_toolset() -> McpToolset:
    """実行中の Python 環境で MCP サーバーを起動するツールセットを作る。"""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=sys.executable,
                args=[str(MCP_SERVER_PATH)],
            ),
        ),
    )
