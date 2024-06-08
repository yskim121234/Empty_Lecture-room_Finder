from tkinter import *

class Search(LabelFrame):
    def __init__(self, root, EnterFunc):
        # 텍스트 입력을 받기 위한 위젯
        self.search = Entry(root, text = "검색")
        self.search.place(x=50, y=60, width=400, height=25)

        # 아이콘
        self.search_icon = PhotoImage(file="./resource/Search_Icon.png").subsample(50, 50)

        # 장식
        canvas1 = Canvas(root, width=500, height=3, bg='black')
        canvas1.place(x=0, y=50)

        canvas2 = Canvas(root, width=500, height=3, bg='black')
        canvas2.place(x=0, y=90)

        # 검색어 입력 후 엔터(업데이트)를 위한 버튼
        self.enter = Button(root, command= EnterFunc, image= self.search_icon)
        self.enter.place(x = 13, y = 58, width= 30, height= 30)