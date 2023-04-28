import pandas as pd

from time import sleep
from datetime import date, timedelta,datetime
from pendulum.tz.timezone import Timezone
# import openpyxl

kst=Timezone('Asia/Seoul')

class finalProcessing:

    def fin_func(self,starttime):
        # 파일 읽기
        AM = pd.read_csv('news2/subpackages/tmp_result/result_AM.csv',encoding="utf-8-sig")
        PM = pd.read_csv('news2/subpackages/tmp_result/result_PM.csv',encoding="utf-8-sig")

        # 병합 및 중복제거
        result = pd.concat((AM,PM),axis=0)
        result.drop_duplicates(subset = 'title', keep='last',inplace = True)

        # 정렬
        result.sort_values(by=[],ascending=[True,True])

        # 저장
        result.to_csv(f'news2/daily_result/result_{starttime}.csv',index=False, encoding="utf-8-sig")
