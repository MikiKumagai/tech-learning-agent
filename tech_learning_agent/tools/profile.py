import json
from pathlib import Path


def get_skill_profile() -> dict:
    """
    ユーザーのスキル・経験・学習目標を取得するTool。
    """
    profile_path = Path(__file__).resolve().parents[2] / "data" / "profile.json"

    with profile_path.open(encoding="utf-8") as f:
        return json.load(f)