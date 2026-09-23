"""ADK が読み込むメインエージェント。"""

from google.adk.agents import Agent

from .config import MODEL
from .sub_agents import learning_planner, technology_evaluator, trend_researcher

root_agent = Agent(
    name="tech_learning_agent",
    model=MODEL,
    description="技術学習を支援するメインAIエージェント",
    instruction="""
    あなたは技術学習を支援するメインエージェントです。

    ユーザーが最近の技術トレンドや学ぶべき技術について質問した場合、

    1. trend_researcher に技術トレンドを調査させる
    2. technology_evaluator に技術候補を評価させる
    3. learning_planner に学習する順番を考えさせる
    4. それぞれの結果を整理してユーザーに回答する

    という流れで対応してください。

    """,
    sub_agents=[
        trend_researcher,
        technology_evaluator,
        learning_planner,
    ],
)
