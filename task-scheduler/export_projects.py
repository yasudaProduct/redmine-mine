import os
import logging
import csv
import pandas as pd
from redminelib import Redmine
from datetime import datetime

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/export.log'),
        logging.StreamHandler()
    ]
)

# 環境変数の取得
REDMINE_URL = os.getenv('REDMINE_URL')
REDMINE_API_KEY = os.getenv('REDMINE_API_KEY')

# Redmineクライアントの初期化
redmine = Redmine(REDMINE_URL, key=REDMINE_API_KEY)

def export_projects():
    """プロジェクト情報をCSVに出力"""
    try:
        # プロジェクト一覧を取得
        projects = redmine.project.all()
        
        # 出力ファイル名を設定（日時を含める）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'/app/data/projects_{timestamp}.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'identifier', 'description', 'homepage', 
                         'status', 'created_on', 'updated_on', 'parent_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for project in projects:
                writer.writerow({
                    'id': project.id,
                    'name': project.name,
                    'identifier': project.identifier,
                    'description': project.description,
                    'homepage': project.homepage,
                    'status': project.status,
                    'created_on': project.created_on,
                    'updated_on': project.updated_on,
                    'parent_id': project.parent.id if hasattr(project, 'parent') and project.parent else ''
                })
        
        logging.info(f"プロジェクト情報を {output_file} に出力しました")
        
        # プロジェクト数を表示
        logging.info(f"出力したプロジェクト数: {len(projects)}")
        
        return output_file
        
    except Exception as e:
        logging.error(f"プロジェクト情報の出力中にエラーが発生しました: {str(e)}")
        return None

def export_trackers():
    """トラッカー情報をCSVに出力"""
    try:
        # トラッカー一覧を取得
        trackers = redmine.tracker.all()
        
        # 出力ファイル名を設定（日時を含める）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'/app/data/trackers_{timestamp}.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'description', 'default_status_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tracker in trackers:
                writer.writerow({
                    'id': tracker.id,
                    'name': tracker.name,
                    'description': tracker.description,
                    'default_status_id': tracker.default_status_id
                })
        
        logging.info(f"トラッカー情報を {output_file} に出力しました")
        
        # トラッカー数を表示
        logging.info(f"出力したトラッカー数: {len(trackers)}")
        
        return output_file
        
    except Exception as e:
        logging.error(f"トラッカー情報の出力中にエラーが発生しました: {str(e)}")
        return None

def export_users():
    """ユーザー情報をCSVに出力"""
    try:
        # ユーザー一覧を取得
        users = redmine.user.all()
        
        # 出力ファイル名を設定（日時を含める）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'/app/data/users_{timestamp}.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'login', 'firstname', 'lastname', 'mail', 'admin', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for user in users:
                writer.writerow({
                    'id': user.id,
                    'login': user.login,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'mail': user.mail,
                    'admin': user.admin,
                    'status': user.status
                })
        
        logging.info(f"ユーザー情報を {output_file} に出力しました")
        
        # ユーザー数を表示
        logging.info(f"出力したユーザー数: {len(users)}")
        
        return output_file
        
    except Exception as e:
        logging.error(f"ユーザー情報の出力中にエラーが発生しました: {str(e)}")
        return None

def export_issue_statuses():
    """チケットステータス情報をCSVに出力"""
    try:
        # ステータス一覧を取得
        statuses = redmine.issue_status.all()
        
        # 出力ファイル名を設定（日時を含める）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'/app/data/issue_statuses_{timestamp}.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'is_closed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for status in statuses:
                writer.writerow({
                    'id': status.id,
                    'name': status.name,
                    'is_closed': status.is_closed
                })
        
        logging.info(f"チケットステータス情報を {output_file} に出力しました")
        
        # ステータス数を表示
        logging.info(f"出力したステータス数: {len(statuses)}")
        
        return output_file
        
    except Exception as e:
        logging.error(f"チケットステータス情報の出力中にエラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "projects":
            export_projects()
        elif command == "trackers":
            export_trackers()
        elif command == "users":
            export_users()
        elif command == "statuses":
            export_issue_statuses()
        elif command == "all":
            export_projects()
            export_trackers()
            export_users()
            export_issue_statuses()
    else:
        # デフォルトではすべての情報を出力
        export_projects()
        export_trackers()
        export_users()
        export_issue_statuses() 