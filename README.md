## 機能

- 定期的なタスク作成機能（スケジューラー）
- プロジェクト情報の CSV エクスポート機能

## 必要条件

- Docker
- Docker Compose

## 使用方法

### 定期的なタスク作成

定期的なタスクを作成する：

```bash
./task-scheduler/run_task.sh init
```

完了したチケットをチェックし、次の定期タスクを作成する：

```bash
./task-scheduler/run_task.sh check
```

### プロジェクト情報のエクスポート

プロジェクト情報を CSV にエクスポートする：

```bash
./task-scheduler/run_task.sh export
```

エクスポートされた CSV ファイルは `task-scheduler/data/` ディレクトリに保存されます。

## ディレクトリ構造

```
redmine-mine/
├── compose.yml          # Docker Compose設定ファイル
├── .env                 # 環境変数設定ファイル
├── README.md            # このファイル
└── task-scheduler/      # タスクスケジューラー関連ファイル
    ├── Dockerfile       # タスクスケジューラーのDockerfile
    ├── requirements.txt # Python依存関係
    ├── scheduler.py     # 定期的なタスク作成スクリプト
    ├── export_projects.py # プロジェクト情報エクスポートスクリプト
    ├── run_task.sh      # タスク実行スクリプト
    ├── data/            # エクスポートされたデータ
    └── logs/            # ログファイル
```
