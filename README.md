# NewsCrawler
新闻爬虫，爬取新华网即时新闻。

### 新华网财经新闻的API为
```python
xinhuanet_template_url = "http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum={}&cnt={}&tp=1&orderby=1"
```

## 新华网各类新闻API

            var recommendArr = [ 
                {
                    "name": "recom",
                    "nid": "11138933"
                },
                {
                    "name": "politics",
                    "nid": ["113352", "11147373", "11148835"]
                },
                {
                    "name": "fortune",
                    "nid": ["115062", "11147664", "1111750"]
                },
                {
                    "name": "国际",
                    "nid": "11145724"
                },
                {
                    "name": "网评",
                    "nid": "11145723"
                },
                {
                    "name": "图片",
                    "nid": "11145722"
                },
                {
                    "name": "社会",
                    "nid": "113321"
                },
                {
                    "name": "法治",
                    "nid": "113207"
                },
                {
                    "name": "local",
                    "nid": "113322"
                },
               {
                    "name": "ent",
                    "nid": "116716"
                }
            ];
## 创建数据库

```mysql
create database news;
use news;
drop table if exists xinhua;
create table xinhua(
Area char(200),
Url char(200),
Time varchar(100),
Title varchar(1000),
Content MEDIUMTEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8;
select * from xinhua;
```

```mysql
drop table if exists xinhua_log;
CREATE table xinhua_log(
    Area char(200),
	Url char(200),	#网址
	Error varchar(500) #错误信息
)ENGINE=InnoDB default charset=utf8;
SELECT * from xinhua_log;
```













