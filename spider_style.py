# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import logging
import urllib2
import re
import os
import time
ori_url="http://www.xiami.com"
start_url="http://www.xiami.com/genre/songs/gid/19?spm=a1z1s.3057857.0.0.j0NopS"
style_page_num=0
style_name=u'中国特色'
while(True):
    style_page_num=style_page_num+1
    urlhd=urllib2.Request(start_url, headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
# The proxy address and port:
# proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}
#
# # We create a handler for the proxy
# proxy_support = urllib2.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
#
# # We create an opener which uses this handler:
# opener = urllib2.build_opener(proxy_support)
# urllib2.install_opener(opener)
    page = urllib2.urlopen(urlhd,timeout=50)
    songs_href = [] 
    songs_list = []
    songs_name_list=[]
    song_list_old = []
    soup = BeautifulSoup(page)
    songs_list_links = soup.findAll('a', href = re.compile(r'/song/.+'))
    for link in songs_list_links:
        if link['href'] not in song_list_old:
            if link['href'] not in songs_list:
                songs_list.append(link['href'])
                songs_name_list.append(link.get_text())
    for index,songs_url in enumerate(songs_list):
        urlhd=urllib2.Request(ori_url+songs_url, headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        sleep_download_time = 1
        time.sleep(sleep_download_time)
        response = urllib2.urlopen(urlhd,timeout=50)
        data = response.read()
        soup2 = BeautifulSoup(data)
        response.close()
        lyrics = soup2.findAll('div',{'class':"lrc_main"})
        if(len(lyrics)==0):
            continue
        p = re.compile('<[^>]+>')
        lrc = p.sub("", str(lyrics[0]))
        if(os.path.exists(os.path.join(os.getcwd(),style_name))==False):
            os.mkdir(os.path.join(os.getcwd(),style_name))
        if(songs_name_list[index].find('/')!=-1):
            songs_name_list[index]=songs_name_list[index].replace('/','and')
        file_object = open(os.path.join(os.getcwd(),style_name+'\\'+songs_name_list[index]+'.txt'), 'w')
        file_object.writelines(lrc.strip())
        file_object.close( )
    if(len(soup.findAll('a',{'class':"p_redirect_l"}))==0 or style_page_num==50):
        break
    else:
        start_url=ori_url+((soup.findAll('a',{'class':"p_redirect_l"}))[0])['href']