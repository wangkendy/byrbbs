#!/usr/bin/env python
import urllib
import json
import urllib2
import cookielib

COOKIEFILE = 'byrbbs.cookie'

def login(uid, passwd):
	posturl = 'http://bbs.byr.cn/user/ajax_login.json'
	params = urllib.urlencode({'id': uid,
			                   'passwd': passwd,
							   'mode':0,
							   'CookieDate': 3})
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('X-Requested-With','XMLHttpRequest')] #this line is critical
	f = opener.open(posturl, params)
	for cookie in cj:
		print cookie.name, cookie.value
	cj.save(COOKIEFILE, ignore_discard=True)
	res_str = f.read()
	res_dic = json.loads(unicode(res_str, 'gbk'))
	if res_dic['ajax_code'] == '0005':
		return True
	else:
		return False
def logout():
	geturl = 'http://bbs.byr.cn/user/ajax_logout.json'
	cj = cookielib.LWPCookieJar()
	cj.load(COOKIEFILE, ignore_discard=True)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('X-Requested-With','XMLHttpRequest')]
	f = opener.open(geturl)
	cj.save(COOKIEFILE, ignore_discard=True)
	res_str = f.read()
	res_dic = json.loads(unicode(res_str, 'gbk'))
	if res_dic['ajax_code'] == '0005':
		return True
	else:
		return False

def post(board='test', subject=None, content=None, pid=0, signature=0):
	'''http://bbs.byr.cn/article/test/ajax_post.json'''
	posturl = 'http://bbs.byr.cn/article/' + board +'/ajax_post.json'
	cj = cookielib.LWPCookieJar()
	cj.load(COOKIEFILE, ignore_discard=True)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
	params = urllib.urlencode({'subject':subject,
							   'content':content,
							   'pid':pid,
							   'signature':signature})
	f = opener.open(posturl, params)
	cj.save(COOKIEFILE, ignore_discard=True)
	res_str = f.read()
	res_dic = json.loads(unicode(res_str, 'gbk'))
	if res_dic['ajax_code'] == '0406':
		return True
	else:
		return False

def upload(filename=None):
	'''http://bbs.byr.cn/att/Picture/ajax_add.json?name=F200907211119482344926889.jpg'''
	if filename == None:
	   err_msg = 'No filename specified'
	   return False, err_msg
	posturl = 'http://bbs.byr.cn/att/Picture/ajax_add.json?name=' + filename
	print 'posturl =', posturl
	cj = cookielib.LWPCookieJar()
	cj.load(COOKIEFILE, ignore_discard=True)
	f = open(filename, 'rb')
	img = f.read()
	print 'len(img)', len(img)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('Content-Length', len(img))]
	opener.addheaders = [('Content-Type', 'application/octet-stream')]
	opener.addheaders = [('Host', 'bbs.byr.cn')]
	opener.addheaders = [('Origin', 'http://bbs.byr.cn')]
	opener.addheaders = [('Referer', 'http://bbs.byr.cn/')]
	opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
	f = opener.open(posturl, img)
	cj.save(COOKIEFILE, ignore_discard=True)
	res_str = f.read()
	res_dic = json.loads(unicode(res_str, 'gbk'))
	if res_dic['ajax_code'] == '0005':
		return True
	else:
		return False

def main():
	res, msg = upload()
	if res:
		print 'upload successfully!'
	else:
		print 'upload failed,' + msg
	return
	if post(board='Picture', subject='test', content='just a test[upload=1][/upload]'):
		print 'post successfully!'
	else:
		print 'post failed!'
	return
	if logout():
		print 'logout successfully!'
	else:
		print 'logout failed!'
	return
	if login('wkendy', '65008540'):
		print 'login successfully!'
	else:
		print 'login failed!'

if __name__ == '__main__':
	main()
