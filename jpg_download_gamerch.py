#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2,os,time
from bs4 import BeautifulSoup

path = '/var/camera/image/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
timesum = 0
dir = 'gamerch'

if (os.path.isdir(path + dir) == False):
	os.system("mkdir " + path + dir)

f = open('./jpg_download_gamerch.txt','r')
for line in f.readlines():
	list = line.split(',')
f.close

for url in list:
	url = "https://xn--eck5eb7eb.gamerch.com/" + url
	start = time.time() #時間開始
	print url + ' Check Start'

	gamerch_dir = dir + "/" + url.split('/')[-1]
	if (os.path.isdir(path + gamerch_dir) == False):
		os.system("mkdir " + path + gamerch_dir)

	os.chdir(path + gamerch_dir)

	webside = urllib2.urlopen(urllib2.Request(url, None, headers), timeout=9999)
	soup = BeautifulSoup(webside, 'html.parser')
	links = soup.findAll('tr')

	img_urls = []
	img_ids = []
	
	#網址擷取
	for link in links:
		img_id = link.find('td')
		img_url = link.find_all('img',attrs={'class':'lazy'})
		if img_url:
			for img_urlbuff in img_url:
				if img_urlbuff['data-original'].startswith('https://cdn.img-conv.gamerch.com/img.gamerch.com/'):
					img_urls.append(img_urlbuff['data-original'])
		else:
			img_urls.append('None')

		if str(img_id) != 'None':
			if int(str(link).find("data-original")) != -1:
				img_ids.append(img_id.text.replace("\n","_") + '-1')
				if img_ids[-1] == '-1':
					img_ids[-1] = img_ids[-2].split("-")[0] + '-2'
				if int(str(link).find("data-original",(int(str(link).find("data-original")) + 1 ))) != -1:
					img_ids.append(img_id.text.replace("\n","_") + '-2')
			else:
				img_ids.append('None')
		else:
			img_ids.append('None')

	for img_id,img_url in zip(img_ids,img_urls):
		if str(img_id) != 'None':
			os.system("wget -q -nc --show-progress -t 5 -T 30 -O " + str(img_id) + "." + str(img_url).split(".")[-1] + " " + str(img_url))

	end = time.time() #時間結束
	timelog = end - start #花費時間
	print url + ' Check End. Time consuming : ' + str(timelog) + ' sec'
	timesum = timesum + timelog

print "Time Sum : " + str(timesum/60) + ' min'