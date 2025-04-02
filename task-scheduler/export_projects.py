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
        
        # 固定の出力ファイル名を設定
        output_file = '/app/data/projects.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'identifier', 'description', 'homepage', 
                         'status', 'created_on', 'updated_on', 'parent_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for project in projects:
                try:
                    parent_id = project.parent.id if hasattr(project, 'parent') and project.parent else ''
                except:
                    parent_id = ''
                
                writer.writerow({
                    'id': project.id,
                    'name': project.name,
                    'identifier': project.identifier,
                    'description': project.description,
                    'homepage': project.homepage,
                    'status': project.status,
                    'created_on': project.created_on,
                    'updated_on': project.updated_on,
                    'parent_id': parent_id
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
        
        # 固定の出力ファイル名を設定
        output_file = '/app/data/trackers.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tracker in trackers:
                try:
                    writer.writerow({
                        'id': tracker.id,
                        'name': tracker.name
                    })
                except Exception as e:
                    logging.warning(f"トラッカー {tracker.id} の処理中にエラーが発生しました: {str(e)}")
                    continue
        
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
        # ユーザー一覧を取得（管理者権限が必要な場合は別の方法を検討）
        try:
            users = redmine.user.all()
        except Exception as e:
            logging.warning(f"ユーザー一覧の取得に失敗しました: {str(e)}")
            # 管理者ユーザーのみ取得を試みる
            users = [redmine.user.get(1)]  # 管理者ユーザーIDを1と仮定
        
        # 固定の出力ファイル名を設定
        output_file = '/app/data/users.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'login', 'firstname', 'lastname', 'mail']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for user in users:
                try:
                    writer.writerow({
                        'id': user.id,
                        'login': user.login,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'mail': user.mail
                    })
                except Exception as e:
                    logging.warning(f"ユーザー {user.id} の処理中にエラーが発生しました: {str(e)}")
                    continue
        
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
        
        # 固定の出力ファイル名を設定
        output_file = '/app/data/issue_statuses.csv'
        
        # CSVファイルに書き込み
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'is_closed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for status in statuses:
                try:
                    writer.writerow({
                        'id': status.id,
                        'name': status.name,
                        'is_closed': status.is_closed
                    })
                except Exception as e:
                    logging.warning(f"ステータス {status.id} の処理中にエラーが発生しました: {str(e)}")
                    continue
        
        logging.info(f"チケットステータス情報を {output_file} に出力しました")
        
        # ステータス数を表示
        logging.info(f"出力したステータス数: {len(statuses)}")
        
        return output_file
        
    except Exception as e:
        logging.error(f"チケットステータス情報の出力中にエラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    # 各エクスポート関数を実行し、エラーが発生しても続行
    success = True
    
    try:
        export_projects()
    except Exception as e:
        logging.error(f"プロジェクト情報のエクスポート中にエラーが発生しました: {str(e)}")
        success = False
    
    try:
        export_trackers()
    except Exception as e:
        logging.error(f"トラッカー情報のエクスポート中にエラーが発生しました: {str(e)}")
        success = False
    
    try:
        export_users()
    except Exception as e:
        logging.error(f"ユーザー情報のエクスポート中にエラーが発生しました: {str(e)}")
        success = False
    
    try:
        export_issue_statuses()
    except Exception as e:
        logging.error(f"チケットステータス情報のエクスポート中にエラーが発生しました: {str(e)}")
        success = False
    
    # いずれかのエクスポートが成功した場合は0を返す
    if success:
        sys.exit(0)
    else:
        sys.exit(1) 