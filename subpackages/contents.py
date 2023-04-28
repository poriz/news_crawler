import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
# import openpyxl

from datetime import date, timedelta,datetime
from time import sleep

timezone = pytz.timezone('Asia/Seoul')

class bringContents:
    def __init__(self):
        self.news_keyword = []
        self.news_dates = []
        self.final_urls = []
        self.news_titles = []
        self.news_contents = []
        self.news_media = []
        self.news_times = []
        self.ex_date = ""
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}


    #####뉴스크롤링 시작#####
    def main(self, key, final_urls_list):
        for url_word in final_urls_list:
            news_time_local=""
            self.news_keyword.append(key)
            self.final_urls.append(url_word) 
            
            try:
                news = requests.get(url_word,headers=self.headers)
            except:
                sleep(1)
                news = requests.get(url_word,headers=self.headers)
                
            news_html = BeautifulSoup(news.text,"html.parser")
        
            # 뉴스 제목 가져오기 
            title = news_html.select_one("")
            if title == None:
                title = news_html.select_one("")
            # 네이버 연예뉴스
            if title == None:
                title = news_html.select_one("")
                title = ' '.join(str(title).split())
            
            # 뉴스 본문 가져오기
            content = news_html.select("")
            if content == []:
                content = news_html.select("")
            # 네이버 연예뉴스
            if content == []:
                content = news_html.select("")
            
            # 언론사 가져오기
            media = news_html.select("")
            if len(media)==0:
                media = news_html.select("")
            
            # 기사 텍스트만 가져오기
            content = ''.join(str(content))
            pattern1 = '<[^>]*>'
            title = re.sub(pattern=pattern1, repl='', string=str(title))
            content = re.sub(pattern=pattern1, repl='', string=content)
            media = re.sub(pattern=pattern1, repl='', string= str(media))
            media = media.strip("[")
            media = media.strip("]")
            media = media.strip("")
            media = media.strip()
            media = media.split(" ")[2]
            content = content.split('')[0].strip()
            content = ' '.join(content.split())

            try:
                html_date = news_html.select_one("")
                news_date = html_date.attrs['']

            except AttributeError:
                news_date = news_html.select_one("")

            if news_date is not None:

                news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
                news_date = news_date.strip()

            else:
                # 네이버 연예뉴스
                news_date = news_html.select_one("")
                news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
            #print(news_date)


            #control dates
            dates_list = news_date.split(" ")
            hour_list = ['10','11','12']
            if len(dates_list) == 3:
                news_date = dates_list[0][:10]
                news_date = re.sub(r'[.]','-',news_date)
                time = dates_list[2].split(":")
                h = int(time[0])
                m = time[1]
                if dates_list[1] == '오후' and h != 12 :
                    h += 12
                else:
                    if str(h) not in hour_list:
                        h = '0' + str(h)
                news_time_local = str(h) + ':' + m + ':00'
            elif len(dates_list) == 2:
                news_date = dates_list[0][:10]
                news_time_local = dates_list[1]

            self.news_media.append(media)
            self.news_titles.append(title)
            self.news_contents.append(content)
            self.news_dates.append(news_date)
            self.news_times.append(news_time_local)

    def split_drop(self, proto_times):
        result_time = int(proto_times.split(":")[0])
        if result_time >8:
            return result_time

    def make_contents(self,execution_date):
        with open('news/subpackages/url_dict.json', 'r') as f:
            url_dict = json.load(f)

        for key,value in url_dict.items():
            self.main(key,value)

        data = {'keyword':self.news_keyword,'news_date':self.news_dates,'news_time':self.news_times ,'media':self.news_media,'link':self.final_urls,'title':self.news_titles,'content':self.news_contents}
        news_df_1 = pd.DataFrame(data, index=range(len(self.news_keyword)))
        news_df = news_df_1.drop_duplicates(subset = 'content',keep='first',ignore_index=True)


        # 오후에 하는경우에만 drop 수행(08시 이전 제거)
        if execution_date =='PM':
            news_df[''] = news_df[''].apply(self.split_drop)
            news_df = news_df.dropna()
            news_df.drop('',axis=1,inplace=True)

        news_df.to_csv(f'news2/subpackages/tmp_result/result_{execution_date}.csv',index=False, encoding="utf-8-sig")

        # 분기를 위한 코드
        time_data ={"data":execution_date}
        with open('news2/subpackages/execution_time.json', 'w') as f:
            json.dump(time_data, f)



                
