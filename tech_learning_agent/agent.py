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
    以下の順番でサブエージェントを利用してください。

    1. trend_researcher
       最新の技術トレンドや学習候補を調査させる。

    2. technology_evaluator
       trend_researcherの調査結果をもとに、
       ユーザーのスキルや目的との関連性を評価させる。
       また、GitHubの公開リポジトリを確認し、
       学習テーマに関連する既存リポジトリを調査させる。

    3. learning_planner
       technology_evaluatorの評価結果とGitHubリポジトリの調査結果をもとに、
       学習計画を作成させる。

       学習計画では、
       - 学習する技術
       - 学習する順番
       - 学習内容
       - 実践方法
       - 既存リポジトリに組み込むか
       - 新しいリポジトリを作成するか
       を検討してください。

    各サブエージェントの結果を次のサブエージェントに渡し、
    前のサブエージェントが調査・判断した内容を踏まえて
    次の処理を行ってください。

    最後に、各結果を整理してユーザーに分かりやすく回答してください。
    """,
    sub_agents=[
        trend_researcher,
        technology_evaluator,
        learning_planner,
    ],
)
