# News Crawler

News module of rate-assistant app
## Author
xiao tang
## Resource
- Chinese:
	- sina: http://cre.dp.sina.cn/api/v3/get?callback=jQuery2140042511583927003604_1486628904032&cateid=y&cre=tianyi&mod=wfin&merge=3&statics=1&impress_id=null%2C&action=0&up=0&down=0&tm=1486628887&_=1486628904033
	- 163: return homepage, http://3g.163.com/touch/money
	- FX168: http://wap.fx168.com/m/news/ JSON analysis
	- this link: http://3g.163.com/touch/reconstruct/article/list/BA8EE5GMwangning/0-10.html
	- sohu: no cover img, http://m.sohu.com/cr/5
POST:[title, puddata, source, cover, url, lan, content]
- Japanese: yahoo.co.jp http://news.yahoo.co.jp/hl?c=bus&p=1
- English: google https://news.google.com/news

## Work to do
- database design (LAMP stack done!)
- python post to JAVAweb API (http request)
- web content storage method:attribute json 
- Need to catch the Json package or some other files the host returned that contains Newslist

## New discoveries
- New crawling local file in Chrome network, json files
	- http://wap.fx168.com/m/mbcf/news/fx168_cpb_zixun_suoyouxinxi_json.html [title, url, imgurl]
