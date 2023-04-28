Airflow를 활용하여 news_data를 주기마다 크롤링하는 코드입니다.

<개발 환경>
WSL2 - Ubuntu 20.04.06
apache-airflow==2.5.2
python3 3.8.10

라이브러리: pandas, openpyxl, sentence-transformers, airflow, bs4, requests,Timezone


<작동 방식>
- Airflow를 통해 schedule되어 스케쥴 된 시간마다 자동으로 작동합니다.
1. links를 통해 키워드에 맞는 링크를 json형태로 저장
2. contents에서 json의 링크들을 읽고, 이를 토대로 뉴스기사 내용을 수집 및 전처리하여 csv파일로 저장
3. branchOperator에서 시간을 확인 후, DAG를 종료시킬지, 다음 task로 진행시킬지 처리.
4. final_processing에서 오전, 오후 파일을 확인 후 중복 제거 및 병합
5. sentence-transformers를 사용하여 문장의 유사도를 측정 하고, utils의 community detection기능을 활용하여 유사도가 높은 문장들로 클러스터링
6. 클러스터별로 조건에 맞는 기사 하나를 추출하여 최종 결과를 도출한다.

