"""技術調査・評価・学習計画を担当するサブエージェント。"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .config import MODEL_NAME
from .tools.profile import get_skill_profile

trend_researcher = Agent(
    name="trend_researcher",
    model=MODEL_NAME,
    description="最新の技術トレンドを調査する",
    instruction="""
    最新の技術トレンドを調査してください。
    Google検索を使って情報を収集し、
    可能な限り公式情報を優先してください。
    """,
    tools=[google_search],
)

technology_evaluator = Agent(
    name="technology_evaluator",
    model=MODEL_NAME,
    description="技術候補をユーザーのスキルや目的に照らして評価するサブエージェント",
    instruction="""
    あなたは技術評価を担当するサブエージェントです。

    まず get_skill_profile を使ってユーザーの現在のスキルを確認してください。

    その上で、渡された技術候補について、

    - 現在のスキルとの関連性
    - データエンジニアとしての関連性
    - 実務で活用できる可能性
    - 必要な前提知識
    - 学習コスト

    を整理してください。

    判断理由も説明してください。
    """,
    tools=[get_skill_profile],
)

learning_planner = Agent(
    name="learning_planner",
    model=MODEL_NAME,
    description="学習する技術の順番と学習計画を作成するサブエージェント",
    instruction="""
    あなたは学習計画の作成を担当するサブエージェントです。

    技術評価の結果をもとに、
    ユーザーが効率よく学習できる順番を考えてください。

    以下の観点で学習計画を作成してください。
    - 学習する技術
    - 学習する順番
    - 各技術を学ぶ理由
    - 先に必要な前提知識
    - 実際に手を動かす学習内容
    - 次の技術へ進む条件

    ユーザーの現在のスキルを考慮し、
    すでに十分な経験がある内容はできるだけ省略してください。

    単に技術を並べるのではなく、
    「なぜこの順番なのか」が分かる学習計画にしてください。
    """,
)
