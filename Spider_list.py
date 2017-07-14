# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import logging
import urllib2
import re
import os
import time
ori_url="http://www.xiami.com"
start_url="http://www.xiami.com/search/collect/page/7?spm=a1z1s.3065917.0.0.qJaZK3&key=%E4%B8%AD%E5%9B%BD%E9%A3%8E&order=weight"
list_page_num=0
style_name=u'ÖÐ¹ú·ç'
while(True):
    list_page_num=list_page_num+1
    list_list=[]
    list_name_list=[]
    urlhd=urllib2.Request(start_url, headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            })
    page = urllib2.urlopen(urlhd,timeout=50)
    soup = BeautifulSoup(page)
    list_links = soup.findAll('div',{'class':"block_cover"})
    for link in list_links:
        list_list.append(link.contents[1]['href'])
        list_name_list.append(link.contents[1]['title'])
    for index,list_url in enumerate(list_list):
        urlhd=urllib2.Request(list_url, headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            })
        page = urllib2.urlopen(urlhd,timeout=50)
        songs_href = [] 
        songs_list = []
        songs_name_list=[]
        song_list_old = []
        soup2 = BeautifulSoup(page)
        page.close()
        songs_list_links = soup2.findAll('span',{'class':"song_name"})
        for link in songs_list_links:
            if(str(link.contents[1]).find('href')==-1):
                continue
            if link.contents[1]['href'] not in song_list_old:
                if link.contents[1]['href'] not in songs_list:
                    songs_list.append(link.contents[1]['href'])
                    songs_name_list.append(link.contents[1]['title'])
        if(len(songs_list)==0):
            continue
        for index,songs_url in enumerate(songs_list):
            if(songs_url.find('www.xiami.com')!=-1):
                continue
            urlhd=urllib2.Request(ori_url+songs_url, headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            })
            sleep_download_time = 0.1
            time.sleep(sleep_download_time)
            response = urllib2.urlopen(urlhd,timeout=50)
            data = response.read()
            soup3 = BeautifulSoup(data)
            response.close()
            lyrics = soup3.findAll('div',{'class':"lrc_main"})
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
    if(len(soup.findAll('a',{'class':"p_redirect_l"}))==0 or list_page_num==50):
        break
    else:
        start_url=ori_url+((soup.findAll('a',{'class':"p_redirect_l"}))[0])['href']