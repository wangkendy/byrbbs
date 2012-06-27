#!/usr/bin/env python
import urllib
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
	opener.addheaders = [('X-Requested-With','XMLHttpRequest')]
	f = opener.open(posturl, params)
	for cookie in cj:
		print cookie.name, cookie.value
	cj.save(COOKIEFILE, ignore_discard=True)
	print f.read()

def main():
	login('wkendy', '65008540')

if __name__ == '__main__':
	main()
