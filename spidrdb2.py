#!/usr/bin/python
#encoding:utf-8
import simplejson
import time
import urllib2
import re
import pymongo
import sqlite3
import HTMLParser

conn = sqlite3.connect('dd2re3')
c = conn.cursor()
urlstart = 'http://estoresrvice7.dianapk.qihang.us/api/search/?clientid=rvtfeil_1&source=rvt_1&q='
urlend = '&start=0&count=10'
c.execute('''create table if not exists doc(id integer, query text, name text, size text, version text, date text, download text, link text, package_name text,  score real)''') 
a = [0, 'query', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 0]

queriesBook = open("result2")
while True :
	i = queriesBook.readline();
	if len(i) == 0:
		break

	temp = re.match(r'.*=(.*),.*', i)
	query = temp.group(1)
	a[1] = query.decode("utf8")
	print "---\n" + query + "+++\n"

	url5 = urlstart + "" + query + urlend
	f = urllib2.urlopen(url5) #the web page infomation is in html
	jdata = simplejson.load(f)

	for i in range(0, 10):
		idata = simplejson.loads(jdata['items'][i]['caption'])
		a[2] = idata["name"]
		a[3] = idata["size"]
		a[4] = idata["version"]
		a[5] = time.strftime("%Y-%m-%d %X",time.gmtime(idata["update_date"]))
		a[6] = idata["download_count"]
		a[7] = idata["icon_url"]
		a[8] = idata["package_name"]
		c.execute('insert into doc values(?,?,?,?,?,?,?,?,?,?)', a)
		conn.commit()
		a[0] = a[0] + 1
		print a
	f.close()
queriesBook.close()
