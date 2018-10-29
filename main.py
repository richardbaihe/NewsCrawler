# -*- coding: utf-8 -*-

import os, MySQLdb
from utils import news_crawler

# 获取项目路径
project_path = os.path.dirname(os.path.realpath(__file__))
# 获取数据存放目录路径
data_path = os.path.join(project_path, 'data')
news_path = os.path.join(data_path, 'news')
if not os.path.exists(news_path):
    os.mkdir(news_path)
extra_dict_path = os.path.join(data_path, 'extra_dict')

conn = MySQLdb.connect(host='localhost',user='root',passwd='21baishuxuan',db='news',charset='utf8')
cursor = conn.cursor()
cursor.execute('select count(*) from xinhua')
count = cursor.fetchall()
print (str(count[0][0])+' news found')
xinhuanet_news_df = news_crawler.get_latest_news('xinhuanet', (conn,cursor), show_content=True)
news_crawler.save_news(xinhuanet_news_df, os.path.join(news_path, 'xinhuanet_latest_news.csv'))