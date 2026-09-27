# tech-learning-agent

技術トレンドの調査から、自分に合った学習テーマの選定、学習計画の作成までを支援するAIエージェント。

Google ADKとGeminiを使って、複数のサブエージェントが役割分担して技術学習を支援する。

## 概要

技術を学ぶときの、

* 最近どんな技術が注目されているか
* 自分のスキルとどう関係するか
* 何から学ぶべきか

を調べて判断する作業をAIで支援する。

```text
ユーザー
  ↓
tech_learning_agent
  ├─ trend_researcher
  ├─ technology_evaluator
  └─ learning_planner
```

### Agent

| Agent                  | 役割                  |
| ---------------------- | ------------------- |
| `trend_researcher`     | 最新の技術トレンドを調査        |
| `technology_evaluator` | スキル・開発経験をもとに技術候補を評価 |
| `learning_planner`     | 学習する順番と実践内容を作成      |

## MCP

GitHubの公開リポジトリ情報を取得するためにMCPを利用している。

```text
technology_evaluator
        ↓ MCP
   MCP Server
        ↓ HTTP
   GitHub API
```

MCP Serverでは以下のToolを提供している。

* `list_github_repos`：公開リポジトリ一覧を取得
* `get_github_repo`：指定したリポジトリの情報を取得

GitHubの情報をAIから利用しやすい形にすることで、現在の開発経験も技術候補の評価に利用している。

## ディレクトリ構成

```text
tech-learning-agent/
├── data/
│   └── profile.json
├── mcp_server/
│   └── server.py
└── tech_learning_agent/
    ├── agent.py
    ├── config.py
    ├── sub_agents.py
    └── tools/
        ├── mcp.py
        └── profile.py
```

## Setup

```bash
git clone https://github.com/MikiKumagai/tech-learning-agent.git
cd tech-learning-agent

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`.env`にGemini API Keyを設定。

```env
GOOGLE_API_KEY=your-api-key
```

起動：

```bash
adk web
```

## 今後

* 学習管理アプリとの連携
* GitHub Wikiへの学習記録
* 過去の学習内容を考慮した学習テーマの提案
* MCP Toolの追加
* Agentの処理フロー改善
