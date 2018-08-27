# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from Video69vj.items import Video69VjItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import re
import sys
import requests
from contextlib import closing
import os

class A69vjSpider(scrapy.Spider):
    name = '69vj'
    allowed_domains = ['69vj.com']
    start_urls = ['http://www.69vj.com/page/1']

    def parse(self, response):
        urls = response.css('.list-item a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_video)
    
    def parse_video(self,response):
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path = 'C:/Users/yy/AppData/Local/Google/Chrome/Application/chromedriver.exe',
        chrome_options=chrome_options)
        #browser = webdriver.PhantomJS()
        item = Video69VjItem()
        file_name1 = response.css('.container-fluid.section span::text').extract()
        file_name2 = response.css('.heading span::text').extract_first()
        item['file_name'] = file_name1[0]+'/'+file_name1[2]
        #html5播放，所以需要使用Selenium
        browser.get(response.url)
        #切换frame，此frame没有id，没有name，只能用xpath切换，参考https://blog.csdn.net/sunruirui1028/article/details/80756307
        iframe=browser.find_element_by_xpath('//*[@class="video_block"]/div/div/iframe')
        browser.switch_to_frame(iframe)
        video = browser.find_element_by_xpath('//*[@id="video_html5_api"]')
        url = browser.execute_script("return arguments[0].currentSrc;", video)
        print(item['file_name']+url)
        item['file_urls'] = [url]
        item['url'] = response.url
        browser.close()  
        browser.quit()
        item['mp4_name'] = file_name2
        path = 'D:/Spider_download/69vj/'+item['file_name']
        print('%s 开始下载！'%path+'/'+item['mp4_name']+'.mp4')
        for file_url in item['file_urls']:
            referer = item['url']
            try:
                headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36",
            "referer":referer}
                url = file_url
                if os.path.exists(path):
                    headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
                else:
                    os.makedirs(path)
                res = requests.get(url, stream=True, headers=headers)
            # 写入收到的视频数据
                with open(path+'/'+item['mp4_name']+'.mp4', 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    print('%s 下载完成！'%path+'/'+item['mp4_name']+'.mp4')
            except Exception as e:
                print(e)
    