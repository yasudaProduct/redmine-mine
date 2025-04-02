FROM python:3.11-slim

# cronのインストール
RUN apt-get update && apt-get install -y cron curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 初期タスク作成用スクリプトの実行権限を付与
RUN chmod +x /app/init-tasks.sh
RUN chmod +x /app/export.sh

# cronの設定
RUN echo "0 9 * * * cd /app && python scheduler.py check >> /app/logs/cron.log 2>&1" > /etc/cron.d/redmine-scheduler
RUN echo "0 0 * * * cd /app && python export_projects.py all >> /app/logs/cron.log 2>&1" >> /etc/cron.d/redmine-scheduler
RUN chmod 0644 /etc/cron.d/redmine-scheduler
RUN crontab /etc/cron.d/redmine-scheduler

# ログディレクトリの作成
RUN mkdir -p /app/logs && touch /app/logs/cron.log

# 初期タスクの作成とcronの起動
CMD ["sh", "-c", "python check-redmine-config.py && python export_projects.py all && /app/init-tasks.sh && cron -f"] 