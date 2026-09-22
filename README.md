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

作成済みの場合は、有効化だけで構いません。新しいターミナルを開いたときも有効化してください。

### 2. 依存パッケージをインストールする

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` にローカルで確認した依存パッケージのバージョンをまとめています。`mcp` と `anyio` は、後述の MCP クライアントでも使用します。

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

ポートを変更する場合：

```bash
adk web --port 8001
```

この場合は <http://localhost:8001> を開きます。サーバーを停止するときは、起動したターミナルで `Ctrl+C` を押します。

起動方法の詳細は [ADK の Python Quickstart](https://adk.dev/get-started/python/) を参照してください。

## ターミナルで使う（adk run）

プロジェクトのルートで次のコマンドを実行すると、対話形式で質問できます。

```bash
adk run tech_learning_agent
```

終了するときは `Ctrl+C` を押します。

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

`career_goal` 以外は文字列の配列で指定します。現在は、Java・Python・SQL などの経験を持ち、データエンジニアを目指すプロフィールが入っています。ツールは呼び出しごとにファイルを読み込むため、プロフィールの変更だけなら再起動は不要です。

## MCP ツールを単独で確認する

`mcp_server/` には、GitHub の公開リポジトリ情報を取得する MCP サーバーと、動作確認用のクライアントがあります。メインエージェントも同じサーバーに接続します。

仮想環境を有効化し、プロジェクトのルートで実行します。

```bash
python mcp_server/client.py
```

クライアントは実行中の Python とサーバーの絶対パスを使って子プロセスを起動し、標準入出力（stdio）経由で `get_github_repo` を呼び出します。サーバーを別のターミナルで起動する必要はありません。ADK からの接続にも同じ起動方式を使っています。

現在のクライアントは `MikiKumagai/progress_management` を取得します。対象を変更する場合は `mcp_server/client.py` の `owner` と `repo` を編集してください。

| 返り値のキー | 内容 |
| --- | --- |
| `name` / `full_name` | リポジトリ名 / 所有者を含む名前 |
| `description` | 説明 |
| `language` | 主な言語 |
| `stars` / `forks` | スター数 / フォーク数 |
| `url` | GitHub 上の URL |

出力は上記を含む MCP のレスポンスオブジェクトです。単独のクライアント実行には Gemini API キーは不要ですが、GitHub API へのネットワーク接続が必要です。

サンプルは MCP Python SDK v2 の API を使用しています。SDK の詳細は [公式 README](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md) を参照してください。

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
├── tests/
│   └── test_integration.py   # プロフィール・ADK・MCP の検証
└── tech_learning_agent/
    ├── __init__.py
    ├── agent.py              # ADK が読み込むメインエージェント
    ├── config.py             # 共通モデル名・ファイルパス
    ├── sub_agents.py         # 調査・評価・学習計画のエージェント
    └── tools/
        ├── mcp.py            # ADK 用 MCP ツールセットの生成
        └── profile.py        # プロフィール取得ツール
```

## エージェントの設定変更

メインエージェントは `tech_learning_agent/agent.py`、サブエージェントは `tech_learning_agent/sub_agents.py` の各 `Agent(...)` を編集します。共通モデル名とファイルパスは `tech_learning_agent/config.py` にまとめています。

| 項目 | 内容 |
| --- | --- |
| `name` | メインまたはサブエージェントの名前 |
| `model` | `config.py` の `MODEL_NAME` を共通利用。初期値は `gemini-3.8-flash` |
| `description` | エージェントの概要 |
| `instruction` | 各エージェントの役割、処理手順、回答方針 |
| `tools` | 検索やプロフィール取得など、そのエージェントが使用するツール |
| `sub_agents` | メインエージェントに登録するサブエージェント |

全エージェントのモデルを変更するときは、利用する API キーで使えるモデル ID を `config.py` の `MODEL_NAME` に指定してください。編集後は `adk web` または `adk run` を再起動します。

## 検証

```bash
python -m unittest discover -s tests -v
```

プロフィールの再読み込み、別ディレクトリからの ADK 読み込みと MCP ツールの検出、GitHub 情報のレスポンスを確認します。GitHub の応答はテスト用データに置き換えるため、外部 API への通信や Gemini API キーは不要です。

## 困ったとき

| 症状 | 確認すること |
| --- | --- |
| `adk: command not found` | `source .venv/bin/activate` を実行し、依存パッケージをインストールしたか確認 |
| API キーに関するエラー | ルートの `.env` に有効な `GOOGLE_API_KEY` が設定されているか確認 |
| モデルが見つからない・利用できない | `config.py` の `MODEL_NAME` が利用可能なモデル ID か確認 |
| エージェントが選択欄に出ない | `tech_learning_agent` フォルダの親ディレクトリで `adk web` を実行しているか確認 |
| ポートが使用中 | `adk web --port 8001` などで別のポートを指定 |
| プロフィールの読み込みに失敗する | `data/profile.json` が存在し、JSON として正しい形式か確認 |
| MCP の `Client` / `MCPServer` をインポートできない | 仮想環境を有効化し、セットアップ手順の `mcp==2.2.0` が入っているか確認 |
| MCP クライアントのファイルが見つからない | プロジェクトのルートで `python mcp_server/client.py` を実行するか、クライアントの絶対パスを指定 |
| GitHub 情報の取得に失敗する | `owner` / `repo`、公開リポジトリかどうか、ネットワーク接続、GitHub API のレート制限を確認 |

利用可能なオプションは、次のコマンドで確認できます。

```bash
adk web --help
adk run --help
```
