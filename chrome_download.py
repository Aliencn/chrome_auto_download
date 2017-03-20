#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python3.41
'''
pip install requests
pip install requests[socks]
pip install requests[security]
pip install beautifulsoup4
pip install selenium
sudo ln phantomjs /bin/
'''

import requests
import json
import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup

class chrome_download():
    def  __init__(self):
        self.log_init()
        self.chrome_download_dir='download'
        self.chrome_os='win'
        self.chrome_channel='stable'
        self.chrome_ver=None
        self.file_full_path=None
        self.download_url=None

        self.switch=None
        self.service_args=None
        self.proxies=None


    def log_init(self):
        log_dir='log'
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        filename='chrome'
        filename='{}{}.log'.format(filename,time.strftime('%Y%m%d',time.localtime(time.time())))
        logging.basicConfig(filename=os.path.join(log_dir,filename),
                            filemode='a',
                            level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
                            )

    #设置代理
    def set_proxy(self,socks5):
        socks5_host=socks5
        logging.info('set proxy:{}'.format(socks5_host))
        #request proxy
        self.proxies = {
            'http': socks5_host,
            'https': socks5_host
            }
        #webdriver proxy
        self.service_args = ['--proxy={}'.format(socks5_host),'--proxy-type=socks5']
        self.switch = 1
        logging.info('proxy switch:{}'.format(self.switch))

    def test_proxy(self):
            logging.info('test_proxy')
            url='http://members.3322.org/dyndns/getip'
            result=self.request_url(url)
            logging.info('test_proxy:{}'.format(result))
            print(result)

    def request_url(self,url,type=None,try_time=3):
        result=None
        for num in range(try_time):
            logging.info('request_url:{},try:{}'.format(url,try_time))
            try:
                s=requests.session()
                s.keep_alive = False
                if self.switch != None:
                    response=s.get(url,timeout=600,proxies=self.proxies)
                else:
                    response=s.get(url,timeout=600)
                s.close()
                if response.status_code == 200:
                    if type == 'json':
                        result=response.json()
                    elif type == 'text':
                        result=response.text
                    else:
                        result=response.content
                    break
            except Exception as e:
                logging.info(e)
                print(e)
        if result == None:
            logging.info('network failure!!!!!!!')
            print('network failure!!!!!!!')
            sys.exit()
        return(result)

    def webdirver_url(self,url,try_time=3):
        result=None
        for num in range(try_time):
            logging.info('webdirver_url:{},try:{}'.format(url,try_time))
            try:
                if self.switch != None:
                    browser = webdriver.PhantomJS(service_args=self.service_args)
                else:
                    browser = webdriver.PhantomJS()
                browser.set_page_load_timeout(600)
                browser.set_script_timeout(600)
                browser.get(url)
                result=browser.page_source
                browser.quit()
                if BeautifulSoup(result,"html.parser").find('html') != None:
                    break
            except Exception as e:
                logging.info(e)
                print(e)
        if result == None:
            logging.info('network failure!!!!!!!')
            print('network failure!!!!!!!')
            sys.exit()
        return(result)


    #获取最新的chrome版本
    def get_chrome_ver(self):
        logging.info('get_chrome_ver')
        ver=None
        url="http://omahaproxy.appspot.com/all.json"
        chrome_versions=self.request_url(url,type='json')
        for version in chrome_versions:
            for info in version['versions']:
                if info['os']== self.chrome_os and info['channel'] == self.chrome_channel:
                    ver=info['version']
        if ver == None:
            logging.info('get version error!!!!')
            print('get version error!!!!')
            sys.exit()
        self.chrome_ver=ver
        logging.info('get_chrome_ver:{}'.format(ver))
        return(ver)

    #生成文件名
    def set_download_name(self):
        logging.info('set_download_name')
        #获取版本
        if self.chrome_ver == None:self.chrome_ver=self.get_chrome_ver()
        #定义扩展名
        if self.chrome_os == 'win' or self.chrome_os == 'win64':
            extname='exe'
        elif self.chrome_os == 'mac':
            extname='dmg'
        else:
            extname='chrome'
        #拼接文件路径
        filename='chrome_{}_{}_{}.{}'.format(self.chrome_os,self.chrome_channel,self.chrome_ver,extname)
        file_full_path=os.path.join(self.chrome_download_dir,filename)
        self.file_full_path=file_full_path
        logging.info('set_download_name:{}'.format(file_full_path))
        return(file_full_path)

    #获取真实下载地址
    def get_chrome_url(self):
        logging.info('get_chrome_url,chrome_os:{}'.format(self.chrome_os))
        if self.chrome_os == 'win64':
            url='https://www.google.com/intl/zh-CN/chrome/browser/thankyou.html?standalone=1&platform=win64'
        elif self.chrome_os == 'win':
            url='https://www.google.com/intl/zh-CN/chrome/browser/thankyou.html?standalone=1&platform=win'
        elif self.chrome_os == 'mac':
            url='https://www.google.com/intl/zh-CN/chrome/browser/thankyou.html?standalone=1&platform=mac'
        else:
            url='123123123'
            logging.info('version not support!!!!')
            print('version not support!!!!')
            sys.exit()
        #获取真实下载地址
        html=self.webdirver_url(url)
        soup = BeautifulSoup(html,"html.parser")
        result=soup.find('a',class_='retry-link')
        download_url=result.get('href')
        self.download_url=download_url
        logging.info('get_download_url:{}'.format(download_url))
        return(self.download_url)


    def check_download(self):
        logging.info('check_download')
        status=None
        self.get_chrome_ver()
        self.set_download_name()
        if os.path.isfile(self.file_full_path) == False :
            logging.info('new donwload')
            print('new donwload')
            self.get_chrome_url()
            print(self.download_url)
            bin=self.request_url(self.download_url)
            if os.path.isdir(os.path.dirname(self.file_full_path)) == False:
                os.makedirs(os.path.dirname(self.file_full_path))
            with open(self.file_full_path, "wb") as f:
                f.write(bin)
            status=1
            logging.info('donwload sucessfull:{}'.format(self.file_full_path))
        else:
            if os.path.getsize(self.file_full_path) < 40 * 1024 * 1024 :os.remove(self.file_full_path)
            logging.info('no update')
            print('no update')
            status=0
        return(status)


if __name__ == '__main__':

    chrome=chrome_download()
    #设置代理，可选项
    chrome.set_proxy('socks5://127.0.0.1:1080')
    chrome.test_proxy()
    #下载路径
    chrome.chrome_download_dir=r'download'
    #chrome版本，['win','win64','mac']
    chrome.chrome_os='win64'
    #检查新版本，并下载
    chrome.check_download()
