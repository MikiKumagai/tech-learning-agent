import json
from typing import Any

from ..config import PROFILE_PATH


def get_skill_profile() -> dict[str, Any]:
    """ユーザーのスキル・経験・学習目標をファイルから取得する。"""
    with PROFILE_PATH.open(encoding="utf-8") as profile_file:
        return json.load(profile_file)
