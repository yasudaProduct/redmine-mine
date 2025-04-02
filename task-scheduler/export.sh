#!/bin/bash

# コマンドライン引数に基づいて処理を実行
if [ "$1" = "projects" ]; then
    python export_projects.py projects
elif [ "$1" = "trackers" ]; then
    python export_projects.py trackers
elif [ "$1" = "users" ]; then
    python export_projects.py users
elif [ "$1" = "statuses" ]; then
    python export_projects.py statuses
elif [ "$1" = "all" ]; then
    python export_projects.py all
else
    # デフォルトではすべての情報を出力
    python export_projects.py all
fi 