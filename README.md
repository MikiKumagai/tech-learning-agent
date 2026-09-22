# tech-learning-agent

Google の Agent Development Kit（ADK）を使った、技術学習を支援する AI エージェントです。Gemini と Google 検索を使い、技術トレンドの調査、ユーザーのスキルに応じた技術候補の評価、学習計画の作成を行います。

## エージェント構成

メインエージェント `tech_learning_agent` に、次の3つのサブエージェントを登録しています。

| エージェント | 役割 | 使用するツール |
| --- | --- | --- |
| `trend_researcher` | 公式情報を優先して最新の技術トレンドを調査 | `google_search` |
| `technology_evaluator` | 現在のスキル、データエンジニアとの関連性、実務での活用、前提知識、学習コストを評価 | `get_skill_profile` |
| `learning_planner` | 学習順序と理由、実践内容、次の技術へ進む条件を含む学習計画を作成 | なし |

メインエージェントには「調査 → 評価 → 学習計画 → 結果の整理」の順で対応するよう指示しています。処理の引き継ぎは LLM の判断に依存するため、固定順序の実行を保証する構成ではありません。

メインエージェントは MCP 経由の `get_github_repo` も利用し、技術候補に関連する GitHub の公開リポジトリ情報を取得できます。

## 必要なもの

- Python 3.10 以上
- Gemini API キー（[Google AI Studio](https://aistudio.google.com/apikey) で取得）

## セットアップ

以下のコマンドは、プロジェクトのルートディレクトリ（この README がある場所）で実行します。シェルの例は macOS / Linux 向けです。

### 1. 仮想環境を作成・有効化する

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 依存パッケージをインストールする

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` にローカルで確認した依存パッケージのバージョンをまとめています。`mcp` と `anyio` は、後述の MCP クライアントでも使用します。

`google-adk==2.9.2` などのパッケージ名とバージョンは `requirements.txt` に記載します。`.env` には、次の手順の API キーなどの環境変数を設定します。

### 3. API キーを設定する

プロジェクトのルートに `.env` を作成し、次の内容を設定します。すでにある場合は内容を確認してください。

```dotenv
GOOGLE_API_KEY=取得したAPIキー
```

`adk web` / `adk run` の起動時に、ADK が `.env` を読み込みます。現在の `agent.py` 自体には `.env` の読み込み処理はありません。`.env` は `.gitignore` の対象です。API キーをソースコードや README に直接書かないでください。

## ブラウザで使う（adk web）

仮想環境を有効化し、プロジェクトのルートで起動します。

```bash
adk web
```

1. ブラウザで <http://localhost:8000> を開きます。
2. エージェントの選択欄で `tech_learning_agent` を選びます。
3. チャット欄に質問を入力します。

質問例：

```text
データエンジニアを目指しています。最近の技術トレンドを調べ、
現在のスキルに合う技術を評価して、学習する順番と実践課題を提案してください。
```

## スキル・学習目標の設定

`data/profile.json` を編集して、自分の経験や目標を設定します。技術評価エージェントが `get_skill_profile` ツールを通じて、このファイルを読み込みます。

| キー | 内容 |
| --- | --- |
| `career_goal` | 目指す職種・キャリア目標（文字列） |
| `languages` | 使用経験のあるプログラミング言語 |
| `cloud` | 使用経験のあるクラウド |
| `database` | 使用経験のあるデータベース |
| `infrastructure` | インフラ関連のツール |
| `data_tools` | データ関連のツール |
| `experience` | 開発や業務の経験 |
| `learning` | 学習中・学習したい分野 |

## ディレクトリ構成

```text
tech-learning-agent/
├── README.md
├── requirements.txt          # 依存パッケージ
├── .gitignore
├── .env                      # ローカルで作成する API キー設定
├── data/
│   └── profile.json          # スキル・経験・学習目標
├── mcp_server/
│   ├── server.py             # GitHub リポジトリ情報を返す MCP サーバー
│   └── client.py             # MCP ツールの呼び出し確認
└── tech_learning_agent/
    ├── __init__.py
    ├── agent.py              # ADK が読み込むメインエージェント
    ├── config.py             # 共通モデル名・ファイルパス
    ├── sub_agents.py         # 調査・評価・学習計画のエージェント
    └── tools/
        ├── mcp.py            # ADK 用 MCP ツールセットの生成
        └── profile.py        # プロフィール取得ツール
```
