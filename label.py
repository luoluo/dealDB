#!/usr/bin/python
#coding=utf-8

import urllib2
import json
import time
#headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
headers = {'Content-type': 'application/json'}
def post(url, data):
    #data_str = urllib.urlencode(data)
    data_str = json.dumps(data)
    print data_str
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req, data_str)
    print 'test info'
    content = response.read()
    print content
    print 'end'
    return content

def main():
    posturl = "http://10.2.8.160/label/api/task/create"
    data = {
        'owner_id': 1,
        'name': 'test api3',
        'data_type': 'text',
        'conflict_strategy': 0,
        'accept_bar': 1,
        'expire_date': "2012-10-9 7:52",
        'data_source': 'a',
        'answer_type': 'choose',
        'task_type': 'entity',
        'task_format': 'r',
    }

    post(posturl, data)

def test():
    posturl = "http://10.2.8.160/label/api/task/data/insert"
    data = {
        'id': 13,
        'items': ['<html>test1</html>','<html>test2</html>','<html>test3</html>']
    }

    post(posturl, data)

def content_subject():
    posturl = "http://10.2.8.160/label/api/task/data/insert"
    data = {
        'id': 4,
        'items': [{'content': {'id': 1, 'page': '<html>test2</html>'}}]
    }

    post(posturl, data)

def content_case1():
    posturl = "http://10.2.8.166/label/api/task/data/insert"
    data = {
        'id': 6,
        'items': [{'content': {'a': 'test a', 'b': 'test b', 'c': 'http://www.baidu.com'}}]
    }

    post(posturl, data)


def meta():
    posturl = "http://10.2.8.160/label/api/task/type/update"
    data = {
        'name': 'subject',
        'answer_meta': {'effects': ['good', 'bad'], 'problems': ['no title', 'title error']}
    }

    post(posturl, data)

def content_case2():
    posturl = "http://10.2.8.160/label/api/task/data/insert"
    data = {
        'id': 20,
        'items': [{'id': 1, 'name': 'Joy', 'sex': 'femail', 'education': 'xxx university', 'description': 'xxx', 'personal': '<html>xxx<html>', 'homepage': 'http://www.baidu.com'}]
    }

    post(posturl, data)

def content_case3():
    posturl = "http://10.2.8.160/label/api/task/data/insert"
    data = {
        'id': 1,
        'items': [{'content': {'title': 'xxx', 'content': 'xxxJoy', 'c': 'femail'}, 'label_form': {'bools': ['c', 'd'], 'chooses': [{'a': ['g', 'f']}]}}]
    }

    post(posturl, data)

def content_case4():
    posturl = "http://10.2.8.160/label/api/task/data/insert"
    time.sleep(1)
    data = {
        'id': 3,
        'items': [{'content':
            {
                'head': {'id': str(int(time.time() - 100)), 'b': 'Joy', 'c': 'femail'},
                'body': [
                    {'id': str(int(time.time() - 3000)), 'b': 'Joy', 'c': 'femail'},
                    {'id': str(int(time.time() - 2000)), 'b': 'Joy', 'c': 'femail'},
                    {'id': str(int(time.time() - 1000)), 'b': 'Joy', 'c': 'femail'},
                    ]
            }
            }
        ]
    }

def content_case5():
    posturl = "http://10.2.8.166/label/api/task/data/insert"
    data = {
        'id': 6,
        'items': [
			{'content': {'query': 'qq', 'name': 'QQ1', 'version': '2013'}},
			{'content': {'query': 'qq', 'name': 'QQ2', 'version': '2013'}},
			{'content': {'query': 'qq', 'name': 'QQ3', 'version': '2013'}},
			{'content': {'query': 'qq', 'name': 'QQ4', 'version': '2013'}},
			{'content': {'query': 'qq', 'name': 'QQ5', 'version': '2013'}},
			{'content': {'query': 'qq', 'name': 'QQ6', 'version': '2013'}}
		]
    }

    post(posturl, data)


if __name__ == '__main__':
    import sys
    n = sys.argv[1]
    print n
    for i in range(int(n)):
        content_case5()
