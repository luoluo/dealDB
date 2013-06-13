import urllib2, urllib
import simplejson
import sqlite3
url = 'http://10.2.8.166/label/api/task/result?id=7&skip=0&limit=20'
f = urllib2.urlopen(url)
html = f.read()
jhtml = simplejson.loads(html)
con = sqlite3.connect("dd2re3")
cu = con.cursor()
st = cu.execute('select * from doc')
rows = st.fetchall()
for row in rows:
	row_id = row[0]
	com = jhtml['items'][row_id]['label']['choose']
	score = 0
	if com == 'Perfect':
		score = 5
	if com == 'Excellent':
		score = 4
	if com == 'Good':
		score = 3
	if com == 'Fair':
		score = 2
#	print score
	cu.execute('update doc set score = ? where id = ?', (score, row_id))
	con.commit()
