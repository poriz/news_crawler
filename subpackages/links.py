import time
from datetime import date, timedelta, datetime

import json
import re
import requests
from bs4 import BeautifulSoup
from subpackages.keys import KEY

from multiprocessing.pool import ThreadPool
import os


class makeLinks:
    def __init__(self):
        self.ex_date = ""
        self.keys = KEY
        self.links = {}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

    def make_pg_num(self, num):
        if num == 1:
            return num
        elif num == 0:
            return num + 1
        else:
            return num + 9 * (num - 1)

    def make_list(self, content):
        newlists = [x for x in content]
        newlist = [x for x in newlists]
        return newlist

    def news_attrs_crawler(self, articles, attrs):
        attrs_content = [i.attrs for i in articles]
        return attrs_content

    def articles_crawler(self, c_url):
        try:
            original_html = requests.get(c_url, headers=self.headers)
        except:
            try:
                time.sleep(0.5)
                original_html = requests.get(c_url, headers=self.headers)
            except:
                pass

        try:
            html = BeautifulSoup(original_html.text, "html.parser")
            url1 = html.select("")
            url2 = self.news_attrs_crawler(url1, 'href')
        except:
            url2 = -1
        
        return url2

    def make_url(self, search_target, start_pg, end_pg, start_day, end_day):
        if start_pg == end_pg:
            start_page = self.make_pg_num(start_pg)
            url = ""
            return url
        else:
            urls = []
            return urls

    def st(self, url):
        news_url = []
        final_urls = []
        token1 =0

        for i in url:
            data = self.articles_crawler(i)
            if data != -1: 
                try:
                    news_url.append(data)
                except:
                    time.sleep(0.5)
                    news_url.append(data)
            else:
                token1 = -1
        if token1 == 0:
            news_url_1=self.make_list(news_url)
            # 특정 뉴스만 남기기
            for i in news_url_1:
                for j in i:
                    if "" in j['href']:

                        final_urls.append(j['href'])
                    else:
                        pass
        else:
            final_urls = -1
            
        return final_urls
        

    def worker(self):
        today1 = datetime.strptime(self.ex_date, '%Y-%m-%d')
        today2 = datetime.strptime(self.ex_date, '%Y-%m-%d')

        yesterday1 = today1 - timedelta(1)
        today1 = today1.strftime('%Y.%m.%d')
        yesterday1.strftime('%Y.%m.%d')

        if today2.weekday() == 0:
            yesterday1 = today2 - timedelta(2)
            yesterday1 = yesterday1.strftime('%Y.%m.%d')
        else:
            yesterday1 = today2 - timedelta(1)
            yesterday1 = yesterday1.strftime('%Y.%m.%d')

        start_day = today1
        end_day = today1

        page = int(1)
        page2 = int(10)  # 마지막페이지*******
        count=0
        for key in self.keys:
            count+=1
            url_tmp = self.make_url(search_target=key, start_pg=page, end_pg=page2, start_day=start_day,
                                    end_day=end_day)

            final_urls = self.st(url_tmp)
            if (final_urls != (-1)) and (len(final_urls) != 0):
                self.links[key] = final_urls
            else:
                pass
            print(f"running : {count}")



    def make_links_func(self, execution_date):
        self.ex_date = execution_date

        self.worker()


        with open('news2/subpackages/url_dict.json', 'w') as f:
            json.dump(self.links, f)
        


