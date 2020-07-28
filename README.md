# NewsCrawler
Multilingual crawler for http://www.xinhuanet.com.

### News API of xinhuanet
```python
xinhuanet_template_url = "http://qc.wa.news.cn/nodeart/list?nid={}&pgnum={}&cnt={}&tp=1&orderby=1"
```

## Example NodeID

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
                    "name": "International",
                    "nid": "11145724"
                },
                {
                    "name": "Review",
                    "nid": "11145723"
                },
                {
                    "name": "图片",
                    "nid": "11145722"
                },
                {
                    "name": "Society",
                    "nid": "113321"
                },
                {
                    "name": "Law",
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
## Create the database for this crawler

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
	Url char(200),	
	Error varchar(500) 
)ENGINE=InnoDB default charset=utf8;
SELECT * from xinhua_log;
```













