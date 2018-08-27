# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import re
import sys
import requests
from contextlib import closing
import os

class video69vjScrapyPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        pass

def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？*|“<>:/]', '', str(path))
    return path




if __name__ == "__main__":
    a = '我是一个？\*|“<>:/错误的字符串'
    print(strip(a))