# tech-learning-agent

Google の Agent Development Kit（ADK）を使った、技術学習を支援する AI エージェントです。学びたい技術について質問すると、Gemini が初学者にも分かるように説明します。

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
python -m pip install google-adk==2.9.2 python-dotenv==1.2.3
```

上記は README 作成時のローカル環境にインストールされているバージョンです。

### 3. API キーを設定する

プロジェクトのルートに `.env` を作成し、次の内容を設定します。すでにある場合は内容を確認してください。

```dotenv
GOOGLE_API_KEY=取得したAPIキー
```

`agent.py` の `load_dotenv()` が `.env` を読み込みます。`.env` は `.gitignore` の対象です。API キーをソースコードや README に直接書かないでください。

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
Python のリストとタプルの違いを、具体例を使って教えてください。
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

## ディレクトリ構成

```text
tech-learning-agent/
├── README.md
├── .gitignore
├── .env                      # ローカルで作成する API キー設定
└── tech_learning_agent/
    ├── __init__.py
    └── agent.py              # root_agent の定義
```

## エージェントの設定変更

`tech_learning_agent/agent.py` の `root_agent = Agent(...)` を編集します。

| 項目 | 内容 |
| --- | --- |
| `name` | エージェント名（`tech_learning_agent`） |
| `model` | 使用するモデル。現在のコードでは `gemini-3.8-flash` を指定 |
| `description` | エージェントの概要 |
| `instruction` | 回答方針。現在は初学者向けの技術説明を指示 |

モデルを変更するときは、利用する API キーで使えるモデル ID を `model` に指定してください。編集後は `adk web` または `adk run` を再起動します。

## 困ったとき

| 症状 | 確認すること |
| --- | --- |
| `adk: command not found` | `source .venv/bin/activate` を実行し、依存パッケージをインストールしたか確認 |
| API キーに関するエラー | ルートの `.env` に有効な `GOOGLE_API_KEY` が設定されているか確認 |
| モデルが見つからない・利用できない | `agent.py` の `model` が利用可能なモデル ID か確認 |
| エージェントが選択欄に出ない | `tech_learning_agent` フォルダの親ディレクトリで `adk web` を実行しているか確認 |
| ポートが使用中 | `adk web --port 8001` などで別のポートを指定 |

利用可能なオプションは、次のコマンドで確認できます。

```bash
adk web --help
adk run --help
```
