#coding=utf8

# RUN: py.test service_suit1.py --host=182.140.141.49 --envname=telecom.int
# RUN: py.test service_suit1.py --host=182.140.141.48 --envname=telecom.int
# RUN: py.test service_suit1.py --host=estoresrvice7.189store.com --envname=telecom.prod
# RUN: py.test service_suit1.py --host=estoresrvice7.dianapk.qihang.us  --envname=diandian.prod
# RUN: py.test service_suit1.py --host=42.121.117.178 --envname=diandian.prod
# RUN: py.test service_suit1.py --host=172.16.7.41 --envname=diandian.test

import pytest
import time
from datetime import datetime
import logging
import threading
import os
import urllib2
import urllib
import simplejson
import pytest

TEST_LOG_DIR = '/tmp/testlog/'

#SERVICE_HOST = {'host': 'http://10.6.8.69', 'is_prod': False}
#SERVICE_HOST = {'host': 'http://182.140.141.11', 'is_prod': True}
#SERVICE_HOST = {'host': 'http://182.140.141.49', 'is_prod': True}
#SERVICE_HOST = {'host': 'http://42.121.117.178', 'is_prod': True}
SERVICE_HOST = {'host': 'http://172.16.7.41', 'is_prod': False, 'envname': 'diandian.test'}

Test_Category = None
Test_Sub_Category = None
Test_Subject = None
Test_App = None

# ~~~~~~~~~~~~~~~~~~~~~~~~NOT COVEREED APIs
#^api/ ^updateservice.json
#^api/ ^crash_report/$
#^api/ ^app/reviews.json

def test_setup(host, envname):
    if not host.startswith('http://') and not host.startswith('https://'):
        host = 'http://' + host
    SERVICE_HOST['host'] = host
    SERVICE_HOST['envname'] = envname
    SERVICE_HOST['is_prod'] = envname.find('prod') != -1

    if not os.path.exists(TEST_LOG_DIR):
        os.makedirs(TEST_LOG_DIR)
    logging.basicConfig(filename=TEST_LOG_DIR + str(long(time.time())) + '.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('service host: ' + str(SERVICE_HOST['host']))
    logging.info('service is_prod: ' + str(SERVICE_HOST['is_prod']))

def build_api_url(api, args = None):
    url = SERVICE_HOST['host'] + '/api/' + api
    if args is not None:
        url = url + '?' + urllib.urlencode(args)
    return url

def call_service_api_raw(api, args, method = 'GET'):
    url = build_api_url(api)
    data = urllib.urlencode(args) if args else None

    logging.info('url=%s, data=%s, method=%s', url, data, method)

    if method == 'GET':
        if data:
            url += '?' if url.find('?') == -1 else '&'
            url += data;
        connection = urllib2.urlopen(url)
    elif method == 'POST':
        connection = urllib2.urlopen(url, data)
    else:
        assert False


    code = connection.getcode()
    assert code == 200

    text = connection.read()
    connection.close()

    logging.info('return: %s', text)
    return text

def call_service_api(api, args, method = 'GET'):
    return simplejson.loads(call_service_api_raw(api, args, method))

def test_notification():
    # NEED TO UPDATE THIS TEST CASE, when there's real data

    # user message
    result = call_service_api('notification/android/messages.json'
                              , {'clientid' : 'testsuit1', 'usrpn' : '123456789', 'source' : 'na', 'locale' : 'zh_CN', 't' : 1353693055}
                              , 'POST')
    #assert result[1]['message_id'] == 101
    #assert len(result[1]['value']) == 1
    #assert len(result) == 2

    # test device: prepublish message
    result = call_service_api('notification/android/messages.json'
                              , {'clientid' : 'testsuit1-testdevice', 'usrpn' : '123456789', 'source' : 'na', 'locale' : 'zh_CN', 't' : 1353693055}
                              , 'POST')
    #assert len(result) == 2

    # blacklist device
    result = call_service_api('notification/android/messages.json'
                              , {'clientid' : 'testsuit1', 'usrpn' : 'testsuit1-phone-in-blacklist', 'source' : 'na', 'locale' : 'zh_CN', 't' : 1353693055}
                              , 'POST')
    #assert len(result) == 0

def test_uploadapplist():
    appinfos = '[{"packageName": "com.fitue.jf.q5", "packageVersion": "100", "packageSig": "-43-54-126-53-35-45-10482121-80116-2283-70-10248104-11953-66", "appName": "Adobe Flash Player 11.1", "packageVersionName" : "1.22.3"}, {"packageName": "com.tripnchat.tripnchat", "packageVersion": "1", "packageSig": "ipa", "appName": "trip and chat", "packageVersionName" : "1.0", "appType":1}]'

    result = call_service_api('app/updates.json'
                              , {'clientid' : 'testsuit1', 'source' : u'com.test.estore_1', 'deviceinfo' : 'Nexus S+4.1.2', 'platform' : 4, 'appinfos' : appinfos}
                              , 'POST')
    assert len(result) == 1
    assert result[0]['version_code'] > 100

    appinfos = '[]'
    result = call_service_api('uploadapplist.json'
                              , {'clientid' : 'testsuit1', 'source' : u'estore 1.0.0', 'deviceinfo' : 'Nexus S+4.1.2', 'appinfos' : appinfos}
                              , 'POST')
    assert len(result) == 1
    assert result[0]['version_code'] > 100

#def test_activities():
#    result = call_service_api('activities.json', {'clientid' : 'testsuit1', 'start_index' : 0, 'count' : 1})
#    assert len(result) == 1
#    assert 'title' in result[0]
#    assert 'icon_url' in result[0]

def test_login_pictures():
    result = call_service_api('login-pictures.json', {'clientid' : 'testsuit1'})
    # not used
    # assert len(result) == 0

def test_feedbacks():
    if SERVICE_HOST['is_prod']:
        print 'skipped for prod env'
        return
    feedbacks = {"user_id": 1234, "content" : "test feedback"}
    result = call_service_api('feedbacks.json'
                              , {'clientid' : 'testsuit1', 'feedback' : simplejson.dumps(feedbacks)}
                              , 'POST')
    assert result is not None
    assert result['ok']

def test_categories():
    global Test_Category, Test_Sub_Category
    result = call_service_api('app/categories.json', {'clientid' : 'testsuit1', 'p_cate_id' : 0, 'start_index' : 0, 'count' : 2})
    assert len(result) == 2
    Test_Category = result[0]['id']
    assert Test_Category is not None
    assert 'icon_url' in result[0]
    assert 'has_child' in result[0]
    assert 'name' in result[0]

    result = call_service_api('app/categories.json', {'clientid' : 'testsuit1', 'p_cate_id' : Test_Category, 'start_index' : 0, 'count' : 2})
    Test_Sub_Category = result[0]['id']
    assert Test_Sub_Category is not None

def test_categories_prod_data():
    if not SERVICE_HOST['is_prod']:
        print 'skipped for test env'
        return
    result = call_service_api('app/categories.json', {'clientid' : 'testsuit1', 'p_cate_id' : 0, 'start_index' : 0, 'count' : 4})
    assert len(result) == 4
    assert (result[0]['id'] == 14334) and (result[0]['name'] == u'应用')
    assert (result[1]['id'] == 14357) and (result[1]['name'] == u'游戏')
    assert (result[2]['id'] == 14371) and (result[2]['name'] == u'阅读')
    assert (result[3]['id'] == 14377) and (result[3]['name'] == u'影音')

def test_category_tops():
    global Test_Category
    if Test_Category is None:
        test_categories()

    result = call_service_api('app/category/tops.json', {'clientid' : 'testsuit1', 'cate_id' : Test_Category, 'start_index' : 0, 'count' : 10})
    assert len(result) == 10
    assert 'version' in result[0]

def test_category_apps():
    global Test_Sub_Category, Test_App
    if Test_Sub_Category is None:
        test_categories()

    result = call_service_api('app/category/apps.json', {'clientid' : 'testsuit1', 'cate_id' : Test_Sub_Category, 'start_index' : 0, 'count' : 10, 'order' : 'downloads'})
    assert len(result) == 10
    assert 'name' in result[0]
    assert 'id' in result[0]
    Test_App = result[0]['id']
    assert Test_App is not None

#def test_focus_images():
#    result = call_service_api('app/category/focus-images.json', {'clientid' : 'testsuit1', 'area' : 'recommend', 'recommend_type' : 'newest', 'start_index' : 0, 'count' : 10})
#    assert len(result) > 0
#
#    global Test_Category
#    if Test_Category is None:
#        test_categories()
#
#    # disabled
#    assert Test_Category is not None
#    result = call_service_api('app/category/focus-images.json', {'clientid' : 'testsuit1', 'area' : 'category', 'cate_id' : Test_Category, 'start_index' : 0, 'count' : 10})
#    assert len(result) == 0
#
#    assert Test_Category is not None
#    result = call_service_api('app/category/focus-images.json', {'clientid' : 'testsuit1', 'area' : 'top', 'cate_id' : Test_Category, 'start_index' : 0, 'count' : 10})
#    assert len(result) > 0

def test_subjects():
    global Test_Subject
#    result = call_service_api('app/subjects.json', {'clientid' : 'testsuit1', 'start_index' : 0, 'count' : 1, 'list_id' : 1})
#    assert result is not None
#    assert len(result) == 1
#    assert 'name' in result[0]
#    assert 'icon_url' in result[0]

#    result = call_service_api('app/subject/apps.json', {'clientid' : 'testsuit1', 'subject_id' : result[0]['id'], 'start_index' : 0, 'count' : 1, 'belong_to' : 2})
#    assert result is not None
#    assert len(result) == 1
#    assert 'name' in result[0]
#    assert 'icon_url' in result[0]

def test_recommends():
    result = call_service_api('app/recommends.json', {'clientid' : 'testsuit1', 'type' : 'newest', 'start_index' : 0, 'count' : 4})
    assert len(result) == 4
    assert 'size' in result[0]


def test_jsonp():
    text = call_service_api_raw('app/recommends.json', {'clientid' : 'testsuit1', 'type' : 'newest', 'start_index' : 0, 'count' : 4, 'callback': 'callbackfunc'})
    assert text.startswith('callbackfunc')

    if SERVICE_HOST['envname'].find('telecom') != -1:
	    pytest.skip('not supported for telecom')

    text = call_service_api_raw('search/', {'clientid' : 'testsuit1', 'q' : 'qq', 'start_index' : 0, 'count' : 8, 'callback': 'searchcallbackfunc'})
    assert text.startswith('searchcallbackfunc')

#def test_mush_haves():
#    result = call_service_api('app/must-haves.json', {'clientid' : 'testsuit1', 'start_index' : 0, 'count' : 4})
#    assert len(result) == 4
#    assert 'version' in result[0]

#def test_bootapps():
#    result = call_service_api('app/bootapps.json', {'clientid' : 'testsuit1', 'osversion' : '4.2', 'devicename' : 'nexus', 'devicetype' : 'test', 'resolution' : '200*300', 'start_index' : 0, 'count' : 1})
#    assert len(result) == 1
#    assert 'version' in result[0]

def test_search_hot_keywords():
    result = call_service_api('app/search/hot-keywords.json', {'clientid' : 'testsuit1', 'start_index' : 10000, 'count' : 5})
    assert len(result) == 5

def test_app_info():
    global Test_App
    if Test_App is None:
        test_category_apps()
    result = call_service_api('app/info.json', {'clientid' : 'testsuit1', 'app_id' : Test_App})
    assert result['id'] == Test_App
    assert 'update_date' in result
    assert 'icon_url' in result
    assert 'size' in result
    assert 'preview_icon_urls' in result
    assert 'version' in result
    assert 'display_download_count' in result
    assert 'name' in result
    assert 'preview_icon_urls' in result
    assert 'small_preview_icon_urls' in result
    assert result['preview_icon_urls'].startswith('http://estoredwnld7.189store.com/')
    # TODO: uncomemnt this, when we have fixed this bug
    # assert result['small_preview_icon_urls'].find('/s_img') != -1
    # assert len(result['related_apps']) > 0
#    related_app = result['related_apps'][0]
#    assert 'icon_url' in related_app
#    assert 'name' in related_app
#    assert 'rate' in related_app

def test_app_download():
    global Test_App
    if Test_App is None:
        test_category_apps()

    # TODO: there is data defect, qpwang/wwenyuan to fix it
    Test_App = 276919

    url = build_api_url('app/download/app.json', {'clientid' : 'testsuit1', 'app_id' : Test_App})
    download_url = urllib2.urlopen(url).geturl()
    assert download_url is not None
    assert download_url.find('.apk') != -1


def test_search():
    query = '1'
    result = call_service_api('search/', {'clientid' : 'testsuit1', 'q' : query, 'start_index' : 0, 'count' : 8})
    assert result['query'] == query
    assert len(result['items']) == 8
    #assert: order by score desc
    for i in range(1, len(result['items'])):
        assert result['items'][i]['score'] <= result['items'][i - 1]['score']
    caption = simplejson.loads(result['items'][0]['caption'])
    assert 'update_date' in caption
    assert 'icon_url' in caption
    assert 'size' in caption
    assert 'version' in caption
    assert 'display_download_count' in caption
    assert 'name' in caption
    assert caption['icon_url'].startswith(u'http://estoredwnld')

def test_blacklist():
    if SERVICE_HOST['envname'].find('telecom') != -1:
        pytest.skip('not supported for telecom')
    result = call_service_api('app/blacklist.json', {'clientid' : 'testsuit1', 'source' : 'com.test_1', 'start_index' : 0})
    assert len([r for r in result if r == 'com.qihoo.appstore']) == 1



################## diandian mobile test cases ##################
def call_service_api_for_diandian(api, args, method = 'GET'):
    return call_service_api('handler/2932ebc6129b27269f70595b04c62b94/com.diandian.appstore.wifi_223/openbox.mobilem.360.cn/' + api, args, method)

def test_diandian_home_subject_list():
    if SERVICE_HOST['envname'].find('telecom') != -1:
        pytest.skip('not supported for telecom')
    result = call_service_api_for_diandian('mintf/getcategorytagsinfobycid'
                              , {'cid' : '5', 'os' : '10', 'start_index' : '0', 'start' : 0, 'count' : 20})
    assert 'errno' in result
    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'category_id' in result['data'][0]
#    assert 'name' in result['data'][0]
#    assert 'url' in result['data'][0]
#    assert 'logo_url' in result['data'][0]

def test_diandian_home_category_list():
    if SERVICE_HOST['envname'].find('telecom') != -1:
        pytest.skip('not supported for telecom')
    result = call_service_api_for_diandian('AppStore/getAllcategory'
                              , {'ring' : '1', 'start' : 0, 'count' : 20})
    assert str(result['errno']) == "0"
    assert len(result['data']['soft']) > 0
    assert len(result['data']['ring']) > 0

    assert 'category_id' in result['data']['soft'][0]
    assert 'name' in result['data']['soft'][0]
    assert 'url' in result['data']['soft'][0]
    assert 'logo_url' in result['data']['soft'][0]

    assert 'category_id' in result['data']['game'][0]
    assert 'name' in result['data']['game'][0]
    assert 'url' in result['data']['game'][0]
    assert 'logo_url' in result['data']['game'][0]

    assert 'category_id' in result['data']['ring'][0]
    assert 'name' in result['data']['ring'][0]
    assert 'url' in result['data']['ring'][0]
    assert 'logo_url' in result['data']['ring'][0]

def test_diandian_spiking_apps():
    if SERVICE_HOST['envname'].find('telecom') != -1:
        pytest.skip('not supported for telecom')
    result = call_service_api_for_diandian('AppStore/getDownloadTrend'
                          , {'cid' : '0', 'os' : 10, 'start' : 0, 'count' : 20})
    assert str(result['errno']) == "0"
    assert len(result['data']) > 0
    assert 'name' in result['data'][0]
    assert 'logo_url' in result['data'][0]

def test_diandian_newest_apps():
    if SERVICE_HOST['envname'].find('telecom') != -1:
        pytest.skip('not supported for telecom')
    result = call_service_api_for_diandian('mintf/getNewApps'
                          , {'cid' : '0', 'os' : 10, 'screen_size' : '854x480', 'start' : 0, 'count' : 20})
    assert str(result['errno']) == "0"
    assert len(result['data']) > 0
    assert 'name' in result['data'][0]
    assert 'logo_url' in result['data'][0]

#def test_diandian_hot_keywords():
#    result = call_service_api_for_diandian('AppStore/getHotWordsIconsOfSearch'
#                          , {'cid' : '0', 'os' : 10, 'screen_size' : '854x480', 'start' : 0, 'count' : 20, 'icon' : '1'})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#
#def test_diandian_search():
#    result = call_service_api_for_diandian('appStore/newSearch?kw=%D0%C2%CE%C5&start=0&count=50&os=10&mid=2932ebc6129b27269f70595b04c62b94'
#                          , {})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][0]
#    assert 'logo_url' in result['data'][0]
#
#def test_diandian_app_details():
#    result = call_service_api_for_diandian('mintf/getAppInfoByIds'
#                          , {'id' : '4889', 'market_id' : 'diandianmarket'})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][0]
#    assert 'logo_url' in result['data'][0]
#
#def test_diandian_app_details_not_exist():
#    result = call_service_api_for_diandian('mintf/getAppInfoByIds'
#                          , {'id' : '34234234', 'market_id' : 'diandianmarket'})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) == 0

#def test_diandian_related_apps():
#    result = call_service_api_for_diandian('AppStore/getRelateAppsById'
#                          , {'id' : '353780', 'os' : 10, 'start' : 0, 'count' : 20})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][0]
#    assert 'logo_url' in result['data'][0]
#
#def test_diandian_developer_apps():
#    result = call_service_api_for_diandian('AppStore/getAppsbyCorp?corp=NUBEE+PTE+LTD&pname=com.nubee.candycandie&type=0&os=10'
#                          , {})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][0]
#    assert 'logo_url' in result['data'][0]

#def test_diandian_app_reviews():
#    result = call_service_api('handler/2932ebc6129b27269f70595b04c62b94/com.diandian.appstore.wifi_223/openbox.comment.mapp.360.cn/message/getmessage/type/best%7Cnormal%7Cbad/name/%E7%94%9C%E8%9C%9C%E5%BD%A9%E7%B3%96/start/0/count/50'
#                          , {})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][0]
#    assert 'logo_url' in result['data'][0]

#def test_diandian_home_recommends():
#    result = call_service_api_for_diandian('AppStore/getNewRecomendApps'
#                          , {'os' : 10, 'screen_size' : '854x480', 'start' : 0, 'count' : 20})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][len(result['data']) - 1]
#    assert 'logo_url' in result['data'][len(result['data']) - 1]
#
#def test_diandian_home_game_recommends():
#    result = call_service_api_for_diandian('AppStore/getGameRecomendApps'
#                          , {'os' : 10, 'screen_size' : '854x480', 'start' : 0, 'count' : 20})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][len(result['data']) - 1]
#    assert 'logo_url' in result['data'][len(result['data']) - 1]
#
#def test_diandian_home_game_top():
#    result = call_service_api_for_diandian('mintf/getAppsByCategory'
#                          , {'cid' : 4, 'csid' : 101620, 'order' : 'download', 'os' : 10, 'screen_size' : '854x480', 'start' : 0, 'count' : 20})
#    assert str(result['errno']) == "0"
#    assert len(result['data']) > 0
#    assert 'name' in result['data'][len(result['data']) - 1]
#    assert 'logo_url' in result['data'][len(result['data']) - 1]
