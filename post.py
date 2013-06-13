#!/usr/bin/python
#coding=utf-8
import json
import time
import urllib
import urllib2
import sqlite3
headers = {'Content-type': 'application/json'}

def post(url, data):
    data_str = json.dumps(data)
#    print data_str
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req, data_str)
#    print 'test info'
    content = response.read()
    print content
    print 'end'

con = sqlite3.connect("dd2re")
cur = con.cursor()
r = cur.execute("select * from doc")
rows = r.fetchall()
#print rows
posturl = "http://10.2.8.166/label/api/task/data/insert"
data = {
    'id': 8,
    'items': [
		{'content': {'query': 'qq', 'name': 'QQ1','size':'', 'version': '2013',
					  'update':'','download':'', 'link':''}},
#		{'content': {'query': 'qq', 'name': 'QQ2', 'version': '2013'}},
#		{'content': {'query': 'qq', 'name': 'QQ3', 'version': '2013'}},
#		{'content': {'query': 'qq', 'name': 'QQ4', 'version': '2013'}},
#		{'content': {'query': 'qq', 'name': 'QQ5', 'version': '2013'}},
#		{'content': {'query': 'qq', 'name': 'QQ6', 'version': '2013'}}
	]
}
idata = {'query':'', 'name':'','size':'', 'version':'','update':'', 'download':'', 'link':'','package_name':''} 
for row in rows:
#19|游戏|街机游戏|5.4M|4.0.1|2013-01-26 05:10:09|656250|http://estoredwnld7.189store.com/img/full/c/59/c597ce53328af92ea24695564410ce00a73f9d38.png|0.0
#0|微博|图钉|7987480|6.2.1|2013-05-24|1111|http://hiphotos.baidu.com/wisegame/pic/item/df3eb13533fa828bf5ff5251fc1f4134960a5aa0.jpg|com.gypsii.activity|0.0

#	print row
	idata['query'] = row[1]
	idata['name'] = row[2]
	idata['size'] = row[3]
	idata['version'] = row[4]
	idata['update'] = row[5]
	idata['download'] = row[6]
#	idata['link'] = '<img src='+ row[6] +' />'
	idata['link'] = row[7]
	idata['package_name'] = row[8]
	data['items'][0]['content'] = idata
	post(posturl, data)

#urllib2.urlopen(r, data)
#h.re
#data = urllib.urlencode(data)
#url = 'http://10.2.8.166/label/api/task/data/insert'
#r = urllib2.Request(url)
