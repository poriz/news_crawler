from time import sleep
from datetime import date, timedelta,datetime
from pendulum.tz.timezone import Timezone
import re
import pandas as pd
import numpy as np
import sys
import os

from sentence_transformers import SentenceTransformer,util


class sts_module:
        
    def model_func(model,titles,thresholds,util):
        
        corpus_sentences = titles
        corpus_embeddings = model.encode(corpus_sentences, batch_size=128, show_progress_bar=True, convert_to_tensor=True)

        clusters = util.community_detection(corpus_embeddings,min_community_size = 1, threshold=thresholds)
        final_titles = []

        for i, cluster in enumerate(clusters):
            count += len(cluster)
            token =0
            result_titles = []
            for sentence_id in cluster:
                result_titles.append(corpus_sentences[sentence_id])
            for tmp_titles in result_titles:
                tmp_df=df2[df2[''].str.contains(tmp_titles)]
                if tmp_df[''].iloc[0] in first_media_list:
                    final_titles.append(tmp_titles)
                    token =1
                elif tmp_df[''].iloc[0] in second_media_list:
                    final_titles.append(tmp_titles)
                    token =1
            if token==0:
                final_titles.append(result_titles[0])

        return final_titles


    def sts_func(self,starttime):

        df = pd.read_csv(f'news2/daily_result/result_{starttime}.csv')

        df[""] = df[""].str.replace(pat=r'[^\w]', repl=r'', regex=True)
        photo_df = df[df[''].str.contains("")]
        df2 = pd.merge(df,photo_df,how='outer',indicator = True)
        df2=df2.query('_merge == "left_only"').drop(columns=['_merge'])


        keywords=set(df2[''])
        titles = df2[''].to_list()
        first_media_list = [""]
        second_media_list = [""]

        df2[""] = df2[""].str.replace(pat=r'\[([^]]+)', repl=r'', regex=True)
        df2[""] = df2[""].str.replace(pat=r"[^\uAC00-\uD7A30-9a-zA-Z]", repl=r' ', regex=True)
        df2[""] = df2[""].str.replace(pat=r"  ", repl=r' ', regex=True)
        df2[""] = df2[""].str.replace(pat=r"   ", repl=r' ', regex=True)

        # Sbert수행
        model = SentenceTransformer("")
        titles = df2[''].to_list()
        # ------------------------------------ 아래부분 반복 수행 3회이상----------------------------------------------------
        threshold_list[0.70,0.66,0.60]
        for threshold in threshold_list:
            titles = model_func(model,titles,threshold,util)

        # 종합
        after_title_df = pd.DataFrame()

        for title in titles:
            tmp=df[df['title'].str.contains(title)]
            if len(tmp) ==0:
                title2 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','', title)
                title2 = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z]", "", title2)
                title2 = title2.replace(r'[^\w]', r'')
                tmp = df[df[''].str.contains(title2)]
            after_title_df = pd.concat((after_title_df,tmp),axis=0)

        result_df = after_title_df.drop_duplicates(subset="")
        result_df.drop(labels='',axis=1,inplace=True)

        # 정렬순서 키워드-날짜-시간
        result_df = result_df.sort_values([''])
        result_df.to_excel(f'news2/final_result/result_{starttime}.xlsx',index=False,encoding='utf-8-sig')


        return 'fin'
