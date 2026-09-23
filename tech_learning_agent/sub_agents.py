"""技術調査・評価・学習計画を担当するサブエージェント。"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .config import MODEL
from .tools.mcp import create_mcp_toolset
from .tools.profile import get_skill_profile

mcp_toolset = create_mcp_toolset()

trend_researcher = Agent(
    name="trend_researcher",
    model=MODEL,
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
    model=MODEL,
    description="技術候補をユーザーのスキルや目的に照らして評価するサブエージェント",
    instruction="""
    あなたは技術評価を担当するサブエージェントです。

    まず get_skill_profile を使ってユーザーの現在のスキルを確認してください。

    次に list_github_repos を owner="MikiKumagai" で呼び出し、
    MikiKumagai が所有する全公開リポジトリを確認してください。
    特定のリポジトリだけに限定せず、取得した一覧全体からスキルや技術候補に関連するリポジトリを探してください。

    必要に応じて get_github_repo を使って、技術候補に関連する GitHub の公開リポジトリ情報を確認してください。
    取得した情報は技術候補の評価に活用し、ユーザーのスキルや目的との関係を分かりやすく説明してください。
    リポジトリ情報にはコード本文は含まれないため、実装内容や習熟度を確認したものとして断定しないでください。

    その上で、渡された技術候補について、

    - 現在のスキルとの関連性
    - データエンジニアとしての関連性
    - 実務で活用できる可能性
    - 必要な前提知識
    - 学習コスト

    を整理してください。

    判断理由も説明してください。
    """,
    tools=[get_skill_profile, mcp_toolset],
)

learning_planner = Agent(
    name="learning_planner",
    model=MODEL,
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

    さらに、学習内容を実践する場所についても検討してください。

    GitHub上の既存リポジトリを確認した結果が渡されている場合は、
    学習テーマとの関連性を考慮し、

    - 既存リポジトリに組み込む
    - 既存リポジトリとは分けて新しいリポジトリを作る

    のどちらが適切か判断してください。

    既存リポジトリに組み込む場合は、
    どのリポジトリに、どのような形で追加するかを具体的に提案してください。

    新しいリポジトリを作る場合は、
    その理由と、どのような構成にすると学習しやすいかを提案してください。

    単にリポジトリを増やすことを目的にせず、
    既存プロジェクトとの関連性や、学習内容を独立して試す必要性を考慮してください。
    """,
)
