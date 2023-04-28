import os
import tkinter.ttk
import threading
import re
import pandas as pd
import time
import shutil
from sentence_transformers import SentenceTransformer, util


from tkinter import *
from tkinter import filedialog


first_media_list = []
second_media_list = []


def th(target_func):
    th = threading.Thread(target=target_func)
    th.daemon = True
    th.start()


def model_func(model, titles, thresholds, util, df2):
    corpus_sentences = titles
    corpus_embeddings = model.encode(corpus_sentences, batch_size=128, show_progress_bar=True, convert_to_tensor=True)
    clusters = util.community_detection(corpus_embeddings, min_community_size=1, threshold=thresholds)
    final_titles = []

    for i, cluster in enumerate(clusters):
        # count += len(cluster)
        token = 0
        result_titles = []
        for sentence_id in cluster:
            result_titles.append(corpus_sentences[sentence_id])
        for tmp_titles in result_titles:
            tmp_df = df2[df2[''].str.contains(tmp_titles)]
            if tmp_df[''].iloc[0] in first_media_list:
                final_titles.append(tmp_titles)
                token = 1
            elif tmp_df[''].iloc[0] in second_media_list:
                final_titles.append(tmp_titles)
                token = 1
        if token == 0:
            final_titles.append(result_titles[0])
    return final_titles


def Sbert_func():
    # 입력파일
    global df, file_date
    time.sleep(1)

    df[""] = df[""].str.replace(pat=r'[^\w]', repl=r'', regex=True)
    photo_df = df[df[''].str.contains("")]
    df2 = pd.merge(df, photo_df, how='outer', indicator=True)
    df2 = df2.query('_merge == "left_only"').drop(columns=['_merge'])

    keywords = set(df2['keyword'])
    titles = df2[''].to_list()

    df2[""] = df2[""].str.replace(pat=r'\[([^]]+)', repl=r'', regex=True)
    df2[""] = df2[""].str.replace(pat=r"[^\uAC00-\uD7A30-9a-zA-Z]", repl=r' ', regex=True)
    df2[""] = df2[""].str.replace(pat=r"  ", repl=r' ', regex=True)
    df2[""] = df2[""].str.replace(pat=r"   ", repl=r' ', regex=True)

    # Sbert수행
    model = SentenceTransformer("")
    titles = df2[''].to_list()
    # ------------------------------------ 아래부분 반복 수행 3회이상----------------------------------------------------
    threshold_list = [0.70, 0.66, 0.60]
    for threshold in threshold_list:
        titles = model_func(model, titles, threshold, util, df2)

    # 종합
    after_title_df = pd.DataFrame()

    for title in titles:
        tmp = df[df['title'].str.contains(title)]
        if len(tmp) == 0:
            title2 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', title)
            title2 = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z]", "", title2)
            title2 = title2.replace(r'[^\w]', r'')
            tmp = df[df[''].str.contains(title2)]
        after_title_df = pd.concat((after_title_df, tmp), axis=0)

    result_df = after_title_df.drop_duplicates(subset="")
    result_df.drop(labels='', axis=1, inplace=True)

    # 정렬순서 키워드-날짜-시간
    result_df = result_df.sort_values([''])
    result_df.to_excel(f'./final_files/final_{file_date}.xlsx', index=False)

    state_1.set(f"수행 완료\n완성파일: final_{file_date}.xlsx")


def open_file():
    global df, file_date, str_1
    root.filename = filedialog.askopenfilename(initialdir='./xlsx', title='파일선택')
    str_1.set(f"file_path: {root.filename}")
    state_1.set("파일 입력완료")
    file_date = root.filename.split('/')[-1].split('.')[0].split('_')[1]
    df = pd.read_excel(root.filename)


def display_state():
    state_1.set("수행중 잠시만 기다려주세요.")


def init_func():
    directory = "./final_files"

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            tkinter.messagebox.showinfo("알림", "초기 설정이 완료되었습니다.")
        else:
            tkinter.messagebox.showinfo("알림", "이미 설정되었습니다.")
    except OSError:
        tkinter.messagebox.showinfo("알림", "설정오류.\n수동으로 'final_files'폴더를\n생성해주세요.")

def auto_func():
    global df
    path=file_path_auto.get()
    execution_time = auto_time.get()

    try:
        if not os.path.exists(path):
            tkinter.messagebox.showinfo("알림", "경로에 폴더가 없습니다.")
        else:
            with open('auto_setup.txt', 'w') as f:
                f.write(f"{path}\n{execution_time}")
            tkinter.messagebox.showinfo("알림", "폴더 설정 완료.")
    except OSError:
        tkinter.messagebox.showinfo("알림", "올바르지 않은 경로입니다.")

def read_me():
    try:
        os.system('readme.txt')
    except:
        tkinter.messagebox.showinfo("알림", "readme파일 없음.")

def auto_start():
    try:
        if os.path.isfile(""):
            print("있음")
            shutil.move("","")
            tkinter.messagebox.showinfo("알림", "설정이 완료되었습니다. 시작프로그램 폴더를 확인해주세요.")
        else:
            tkinter.messagebox.showinfo("알림", "파일이 존재하지 않습니다.\n문의하세요.")
    except:
        tkinter.messagebox.showinfo("알림", "에러발생\n문의하세요.")


if __name__ == '__main__':
    df = pd.DataFrame()
    file_date = ""
    root = Tk()
    root.title('Remove Duplicates(News)')
    root.geometry("800x400")

    str_1 = StringVar()
    str_2 = StringVar()
    str_3 = StringVar()
    state_1 = StringVar()

    str_1.set("파일 열기 버튼을 눌러주세요.")
    str_2.set("자동화 할 폴더 경로 입력")
    str_3.set("파일 실행시간 설정 ex) 17:00")
    state_1.set("대기중")

# ----------------------------------frame--------------------------------------------
    selfFrame= Frame(root,width=1200)
    information_frame = Frame(selfFrame, width=1200, relief='solid')
    left_info_frame = Frame(selfFrame)
    button_frame = Frame(selfFrame)
    auto_frame = Frame(root)

# ----------------------------------contents--------------------------------------------
    # label
    self_info_label = Label(selfFrame,text="------------------------------------------------<수동 영역>------------------------------------------------")
    file_path_label = Label(left_info_frame, text='file_path')
    file_path_label_auto = Label(auto_frame, text='file_path')
    auto_time_lable = Label(auto_frame,text="실행 시간")
    state_label = Label(left_info_frame, text='상태')
    auto_info_label = Label(selfFrame, text="------------------------------------------------<자동 영역>------------------------------------------------")
    program_state = Label(information_frame, textvariable=state_1)

    # entry
    file_path = Entry(information_frame, width=94, textvariable=str_1)
    file_path_auto = Entry(auto_frame, width=103, textvariable=str_2)
    auto_time = Entry(auto_frame, width=103, textvariable=str_3)

    # button
    init_btn = Button(root, text='공통 초기 설정', command=init_func)
    processing_btn = Button(button_frame, text='처리', command=lambda: [display_state(), th(self.Sbert_func)])
    open_btn = Button(button_frame, text='파일열기', command=open_file)
    auto_btn = Button(auto_frame, text='자동 수행 폴더 설정', command=auto_func)
    read_me_btn = Button(auto_frame,text='사용방법',command=lambda : th(read_me))
    auto_start_btn=Button(auto_frame,text='자동 실행',command=lambda : th(auto_start))

# ----------------------------------grid--------------------------------------------
    # self Frame
    selfFrame.grid(row=1,column=0,padx=3,pady=10)
    self_info_label.grid(row=0,column=1,sticky='news')
    information_frame.grid(row=1, column=1, sticky='NEWS', padx=3, pady=10)
    left_info_frame.grid(row=1, column=0, sticky='NEWS', padx=5, pady=10)
    button_frame.grid(row=1, column=2, sticky='NEWS', padx=3, pady=10)
    auto_info_label.grid(row=4, column=1, sticky='news',padx=3)

    # auto frames
    auto_frame.grid(row=2,column=0,sticky='NEWS',columnspan=3,padx=3,pady=1)

    # left_info_frame
    file_path_label.grid(row=0, column=0, sticky='NEWS')
    state_label.grid(row=1, column=0, sticky='NEWS')

    # information_frame
    file_path.grid(row=0, column=1, columnspan=3, sticky='NEWS')
    program_state.grid(row=1, column=1, columnspan=3, sticky='NEWS')

    # button_frame
    open_btn.grid(row=0, column=0, sticky='NEWS')
    processing_btn.grid(row=1, column=0, sticky='NEWS')
    init_btn.grid(row=0, column=0, columnspan=3, sticky='NEWS',padx=3,pady=10)

    # auto_frame
    file_path_label_auto.grid(row=0,column=0,sticky='NEWS',padx=3)
    file_path_auto.grid(row=0,column=1,sticky='NEWS',padx=3)
    auto_time_lable.grid(row=1,column=0,sticky='NEWS',padx=3)
    auto_time.grid(row=1,column=1,sticky='NEWS',padx=3)
    auto_btn.grid(row=2,column=0,columnspan=3,sticky='NEWS')
    auto_start_btn.grid(row=3,column=0,columnspan=3,sticky='news')
    read_me_btn.grid(row=4,column=0,columnspan=3,sticky='NEWS',pady=10)

    root.resizable(False, False)
    root.mainloop()
