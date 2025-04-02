import os
import logging
import pandas as pd
from datetime import datetime, timedelta
from redminelib import Redmine
import psycopg2
from dateutil.relativedelta import relativedelta
import time
import json

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 環境変数取得
REDMINE_URL = os.getenv('REDMINE_URL')
REDMINE_API_KEY = os.getenv('REDMINE_API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Redmineクライアント初期化
redmine = Redmine(REDMINE_URL, key=REDMINE_API_KEY)

def get_db_connection():
    """データベース接続を取得"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def check_completed_issues():
    """完了したチケットをチェックし、次の定期タスクを作成"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 完了したチケットを取得
        cur.execute("""
            SELECT i.id, i.subject, i.description, i.project_id, i.tracker_id,
                   i.assigned_to_id, i.priority_id, i.closed_on
            FROM issues i
            WHERE i.status_id = 5  -- 完了ステータスのID
            AND i.closed_on >= NOW() - INTERVAL '1 day'
        """)
        completed_issues = cur.fetchall()

        # 定期タスクの定義を読み込み
        tasks_df = pd.read_csv('/app/data/periodic_tasks.csv')
        
        for issue in completed_issues:
            # 対応する定期タスク定義を検索
            matching_task = tasks_df[tasks_df['subject'] == issue[1]]
            
            if not matching_task.empty:
                task = matching_task.iloc[0]
                
                # 次回の期日を計算
                if task['interval_type'] == 'monthly':
                    next_date = datetime.now() + relativedelta(months=int(task['interval_value']))
                elif task['interval_type'] == 'weekly':
                    next_date = datetime.now() + timedelta(weeks=int(task['interval_value']))
                
                # 新しいチケットを作成
                new_issue = redmine.issue.create(
                    project_id=int(task['project_id']),
                    subject=task['subject'],
                    description=task['description'],
                    tracker_id=int(task['tracker_id']),
                    assigned_to_id=int(task['assigned_to_id']),
                    priority_id=int(task['priority_id']),
                    start_date=datetime.now().date(),
                    due_date=next_date.date()
                )
                
                logging.info(f"新しい定期タスクを作成しました: {new_issue.id} - {task['subject']}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"エラーが発生しました: {str(e)}")

def create_initial_tasks():
    """CSVファイルから初期タスクを作成する"""
    try:
        # CSVファイルを読み込む
        df = pd.read_csv('/app/data/periodic_tasks.csv')
        
        # 各タスクに対して処理
        for _, row in df.iterrows():
            # 既存のチケットをチェック
            existing_issues = redmine.issue.filter(
                project_id=row['project_id'],
                subject=row['subject']
            )
            
            # 同じ件名のチケットが存在する場合はスキップ
            if len(existing_issues) > 0:
                logging.info(f"スキップ: 件名 '{row['subject']}' のチケットは既に存在します")
                continue
            
            # チケットを作成
            issue = redmine.issue.new()
            issue.project_id = row['project_id']
            issue.subject = row['subject']
            issue.description = row['description']
            issue.tracker_id = row['tracker_id']
            issue.assigned_to_id = row['assigned_to_id']
            issue.priority_id = row['priority_id']
            issue.start_date = row['start_date']
            issue.save()
            
            logging.info(f"チケットを作成しました: {row['subject']}")
            
    except Exception as e:
        logging.error(f"初期タスクの作成中にエラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    # コマンドライン引数に基づいて処理を実行
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "check":
            check_completed_issues()
        elif command == "init":
            create_initial_tasks()
    else:
        logging.error("コマンドを指定してください: check または init") 