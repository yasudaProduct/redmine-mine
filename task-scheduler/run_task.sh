#!/bin/bash

# 使用方法の表示
usage() {
    echo "使用方法: $0 [check|init|export]"
    echo "  check  - 完了したチケットをチェックし、次の定期タスクを作成"
    echo "  init   - 初期の定期タスクを作成"
    echo "  export - プロジェクト情報をCSVにエクスポート"
    exit 1
}

# コマンドライン引数をチェック
if [ $# -eq 0 ]; then
    usage
fi

# コマンドの種類を判定
case "$1" in
    "check"|"init")
        SCRIPT="scheduler.py"
        ;;
    "export")
        SCRIPT="export_projects.py"
        ;;
    *)
        usage
        ;;
esac

# task-schedulerコンテナが実行中かチェック
CONTAINER_RUNNING=$(docker compose ps task-scheduler --format json | grep -c "running")

if [ $CONTAINER_RUNNING -eq 0 ]; then
    echo "task-schedulerコンテナを起動します..."
    docker compose up -d task-scheduler
    
    # コンテナの起動を待機
    echo "コンテナの起動を待機中..."
    sleep 5
fi

# スクリプトを実行
echo "${SCRIPT}を実行します..."
if [ "$1" = "export" ]; then
    docker compose exec task-scheduler python /app/${SCRIPT}
else
    docker compose exec task-scheduler python /app/${SCRIPT} $1
fi

# 実行結果のステータスを保存
STATUS=$?

# コンテナが新しく起動された場合は停止
if [ $CONTAINER_RUNNING -eq 0 ]; then
    echo "task-schedulerコンテナを停止します..."
    docker compose stop task-scheduler
fi

exit $STATUS 