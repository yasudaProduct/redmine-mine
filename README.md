- 定期的なタスク作成機能（スケジューラー）
- プロジェクト情報の CSV エクスポート機能

## 必要条件

- Docker
- Docker Compose

## 使用方法

### 定期的なタスク作成

定期的なタスクを作成するには、以下のコマンドを実行します：

```bash
./task-scheduler/run_task.sh init
```

完了したチケットをチェックし、次の定期タスクを作成するには：

```bash
./task-scheduler/run_task.sh check
```

### プロジェクト情報のエクスポート

プロジェクト情報を CSV にエクスポートするには：

```bash
./task-scheduler/run_task.sh export
```

エクスポートされた CSV ファイルは `task-scheduler/data/` ディレクトリに保存されます。

### 定期タスクの設定

定期タスクは `task-scheduler/data/periodic_tasks.csv` ファイルで管理されています。このファイルには以下の列が含まれています：

| 列名           | 説明                         | 例                         |
| -------------- | ---------------------------- | -------------------------- |
| subject        | タスクの件名                 | 月次報告書作成             |
| description    | タスクの説明                 | 毎月の業務報告書を作成する |
| project_id     | プロジェクト ID              | 1                          |
| tracker_id     | トラッカー ID                | 1                          |
| assigned_to_id | 担当者 ID                    | 1                          |
| priority_id    | 優先度 ID                    | 1                          |
| interval_type  | 間隔の種類（monthly/weekly） | monthly                    |
| interval_value | 間隔の値                     | 1                          |
| start_date     | 開始日（YYYY-MM-DD 形式）    | 2024-04-01                 |

このファイルを編集することで、定期タスクの設定を変更できます。例えば、新しい定期タスクを追加するには、新しい行を追加します。

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
    │   └── periodic_tasks.csv # 定期タスク設定ファイル
    └── logs/            # ログファイル
```
