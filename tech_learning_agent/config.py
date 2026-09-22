"""エージェント共通の設定と、作業ディレクトリに依存しないパス。"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_NAME = "gemini-3.8-flash"
PROFILE_PATH = PROJECT_ROOT / "data" / "profile.json"
MCP_SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"
