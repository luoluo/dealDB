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

con = sqlite3.connect("re2")
cur = con.cursor()
r = cur.execute("select * from doc")
rows = r.fetchall()
#print rows
posturl = "http://10.2.8.166/label/api/task/data/insert"
data = {
    'id': 6,
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
idata = {'query':'', 'name':'','size':'', 'version':'','update':'', 'download':'', 'link':''} 
for row in rows:
#19|游戏|街机游戏|5.4M|4.0.1|2013-01-26 05:10:09|656250|http://estoredwnld7.189store.com/img/full/c/59/c597ce53328af92ea24695564410ce00a73f9d38.png|0.0

#	print row
	idata['query'] = row[1]
	idata['name'] = row[2]
	idata['size'] = row[3]
	idata['version'] = row[4]
	idata['update'] = row[5]
	idata['download'] = row[6]
#	idata['link'] = '<img src='+ row[6] +' />'
	idata['link'] = row[7]
	data['items'][0]['content'] = idata
	post(posturl, data)

#urllib2.urlopen(r, data)
#h.re
#data = urllib.urlencode(data)
#url = 'http://10.2.8.166/label/api/task/data/insert'
#r = urllib2.Request(url)
