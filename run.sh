#!/bin/bash

cd $PROD_PATH
rm -f /app/wechat_report/celery_worker.pid
rm -f /app/wechat_report/celery_beat.pid

# 安装字体
tar -zxf /app/wechat_report/win.tar.gz -C /usr/share/fonts/
cd /usr/share/fonts/win/
mkfontscale
mkfontdir
fc-cache -fv


# 对工具做链接
ln -s /app/wechat_report/wkhtmltox/bin/wkhtmltoimage /usr/local/bin/
ln -s /app/wechat_report/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/
ln -s /app/wechat_report/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/
ln -s /app/wechat_report/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/

# 拷贝生产配置文件
cp /app/config/config.ini $PROD_PATH 

# 启动django
cd /app/DataCenter

python3 manage.py runserver 0.0.0.0:$PROT &

sleep 3

# 启动worker
celery worker -A DataCenter -B -c 1 --max-tasks-per-child 1 -l INFO --pidfile="/app/wechat_report/celery_worker.pid"  --logfile="/var/log/celery_work.log" &

sleep 3

# 启动beat
celery beat -A DataCenter -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile="/app/wechat_report/celery_beat.pid" --logfile="/var/log/celery_beat.log"
