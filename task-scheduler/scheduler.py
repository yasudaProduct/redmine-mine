import os
import logging
import pandas as pd
from datetime import datetime, timedelta
from redminelib import Redmine
import psycopg2
from dateutil.relativedelta import relativedelta
import time
import json

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/scheduler.log'),
        logging.StreamHandler()
    ]
)

# 環境変数の取得
REDMINE_URL = os.getenv('REDMINE_URL')
REDMINE_API_KEY = os.getenv('REDMINE_API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Redmineクライアントの初期化
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
    """初期の定期タスクを作成"""
    try:
        tasks_df = pd.read_csv('/app/data/periodic_tasks.csv')
        
        # プロジェクトの存在確認
        try:
            project = redmine.project.get(1)
            logging.info(f"プロジェクト '{project.name}' が見つかりました")
        except Exception as e:
            logging.error(f"プロジェクトID 1 が見つかりません: {str(e)}")
            return
        
        # トラッカーの存在確認
        try:
            tracker = redmine.tracker.get(1)
            logging.info(f"トラッカー '{tracker.name}' が見つかりました")
        except Exception as e:
            logging.error(f"トラッカーID 1 が見つかりません: {str(e)}")
            return
        
        for _, task in tasks_df.iterrows():
            try:
                # 開始日から次回の期日を計算
                start_date = datetime.strptime(task['start_date'].strip(), '%Y-%m-%d')
                
                if task['interval_type'] == 'monthly':
                    due_date = start_date + relativedelta(months=int(task['interval_value']))
                elif task['interval_type'] == 'weekly':
                    due_date = start_date + timedelta(weeks=int(task['interval_value']))
                
                # チケットを作成
                issue_data = {
                    'project_id': int(task['project_id']),
                    'subject': task['subject'],
                    'description': task['description'],
                    'tracker_id': int(task['tracker_id']),
                    'assigned_to_id': int(task['assigned_to_id']),
                    'priority_id': int(task['priority_id']),
                    'start_date': start_date.date().isoformat(),
                    'due_date': due_date.date().isoformat()
                }
                
                logging.info(f"チケット作成データ: {json.dumps(issue_data, ensure_ascii=False)}")
                
                new_issue = redmine.issue.create(**issue_data)
                
                logging.info(f"初期タスクを作成しました: {new_issue.id} - {task['subject']}")
                time.sleep(1)  # APIレート制限を考慮
                
            except Exception as e:
                logging.error(f"タスク '{task['subject']}' の作成中にエラーが発生しました: {str(e)}")
                continue
            
    except Exception as e:
        logging.error(f"初期タスク作成中にエラーが発生しました: {str(e)}")

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