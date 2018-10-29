# -*- coding:utf-8 -*-

import urllib, urllib.request
from bs4 import BeautifulSoup
import requests
import json
import re
from tqdm import tqdm
from random import randint
from datetime import datetime
import pandas as pd

LATEST_COLS = ['title', 'time', 'url']
LATEST_COLS_C = ['title', 'time', 'url', 'content']
area_nid = [{"name": "推荐","nid": ["11138933"]},
            {"name": "政治","nid": ["113352", "11147373", "11148835"]},
            {"name": "财经","nid": ["115062", "11147664", "1111750"]},
            {"name": "国际","nid": ["11145724"]},
            {"name": "网评","nid": ["11145723"]},
            {"name": "图片","nid": ["11145722"]},
            {"name": "社会","nid": ["113321"]},
            {"name": "法治","nid": ["113207"]},
            {"name": "地方","nid": ["113322"]},
            {"name": "娱乐","nid": ["116716"]}]

xinhuanet_template_url = 'http://qc.wa.news.cn/nodeart/list?nid={}&pgnum={}&cnt={}&tp=1&orderby=1'
nets = ['xinhuanet']

template_urls = {
    'xinhuanet': xinhuanet_template_url
}
latest_news_functions = {
    'xinhuanet': 'get_xinhuanet_latest_news'
}
xpaths = {
    'xinhuanet': '//*[@id="p-detail"]/p'
}


def get_latest_news(net, conn_cursor, show_content=False):
    """
    获取即时新闻（新浪、搜狐、新华网）
    :param net: string，指定网站名
    :param top: 数值，显示最新消息的条数，默认为80条
    :param show_content: 是否显示新闻内容，默认False
    :return: DataFrame
        title: 新闻标题
        time: 发布时间
        url: 新闻链接
        content: 新闻内容（在show_content为True的情况下出现）
    """
    assert net in nets, '参数1(net)错误！应为' + '、'.join(nets) + '中的一个！'
    #latest_news_function = latest_news_functions[net]
    template_url = template_urls[net]
    df_all = []
    for an in area_nid:
        area = an['name']
        for nid in an['nid']:
            print('crawling {} from {}...'.format(nid,area))
            df = get_xinhuanet_latest_news(template_url, area, nid, conn_cursor)
            df_all.append(df)
    df_all = pd.concat(df_all)
    return df_all


def latest_content(net, url):
    """
    获取即时财经新闻内容
    :param net: 指定网站名
    :param url: 新闻链接
    :return: string
        返回新闻的文字内容
    """
    data = ''
    try:
        r = requests.get(url)
        content = r.content
        if net=='renmin':
            start = content.find(b'<!--text_con-->')
            end = content.find(b'paper_num')
            content = content[start:end]
        soup = BeautifulSoup(content, "html.parser")
        for t in soup.find_all('p'):
            data += t.text
        data = re.sub(r'(\r*\n)+', '\n', data)
    except Exception as e:
        return e, -1
    return data, 1


def get_xinhuanet_latest_news(template_url,area, nid, conn_cursor):
    """获取新华网即时新闻"""
    try:
        conn,cursor = conn_cursor
        pgnum = 1
        data = []
        while True:
            cnt = 100
            url = template_url.format(nid, pgnum, cnt)
            pgnum += 1
            request = urllib.request.Request(url)
            data_str = urllib.request.urlopen(request, timeout=10).read()
            data_str = data_str.decode('utf-8')
            data_str = data_str[1:-1]
            data_str = eval(data_str, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
            if data_str['status']==-1:
                break
            data_str = json.dumps(data_str)
            data_str = json.loads(data_str)
            data_str = data_str['data']['list']
            for r in tqdm(data_str):
                rt = datetime.strptime(r['PubTime'], '%Y-%m-%d %H:%M:%S')
                rt_str = datetime.strftime(rt, '%Y-%m-%d %H:%M')
                row = [r['LinkUrl'], rt_str, r['Title']]
                content, status = latest_content('xinhuanet', r['LinkUrl'])
                content = content.replace('\'', '\\\'')
                if status == -1:
                    cursor.execute("insert into xinhua_log values ('%s','%s','%s')" % (
                        area, row[0], content))
                else:
                    row.append(content)
                    data.append(row)
                    cursor.execute(
                        "insert into xinhua values ('%s','%s','%s','%s','%s')" % (
                            area, row[0], row[1], row[2], row[3]))
                conn.commit()
            cursor.execute('select count(*) from xinhua')
            count = cursor.fetchall()
            print(str(count[0][0]) + ' news found')
        df = pd.DataFrame(data, columns=LATEST_COLS_C if show_content else LATEST_COLS)
        return df
    except Exception as e:
        print(e)


def save_news(news_df, path):
    """保存新闻"""
    news_df.to_csv(path, index=False, encoding='gb18030')
    # news_df.to_csv(path, index=False)


def replace_line_terminator(x):
    """替换行终止符"""
    try:
        x = re.sub(r'\r\n', '\n', x)
    except TypeError:
        pass
    return x


def load_news(path):
    """加载新闻"""
    news_df = pd.read_csv(path, encoding='gb18030')
    news_df = news_df.applymap(replace_line_terminator)
    return news_df
