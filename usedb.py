#!/usr/bin/python
import sqlite3
import sys
conn = sqlite3.connect("re1")
c = conn.cursor()
r = c.execute('select * from doc')
rows = r.fetchall()
for row in rows:
	print "query =\t" + row[0] + "\tthe Docs' detail info as follows:"
	print "name:" + row[1] + "\t\t" + row[2] + "\t\t" + row[3] + "\t\t" + row[5] + "\t\ticon_url:\t\t" + row[6]
#	for son in row:
#		print son
	uname = row[1]
	newscore = input('Please enter score for this doc\t' + uname.encode("utf8") + "\n")
#with conn:
	c.execute('update doc set score = ?  where name = ?', (newscore, uname))
	conn.commit()
