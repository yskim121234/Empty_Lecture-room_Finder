from tkinter import *
from functools import partial
from TimeTable_Analyzer import TTAnalyzer as TTA
class Bookmark():
    list = []
    f = open('./Bookmark.txt', 'r')
    line = f.readline()
    list = line.split(',')
    f.close() 
    for i in range(len(list)):
        if list[i] == '':
            del list[i]
    
class Select_room():
    
    def __init__(self):
        # DB에서 모든 강의실을 불러옴
        self.rooms = TTA('./TimeTable_CS.db').Get_All_Room()
        self.Bookmark = Bookmark()
        
    
       
    # 강의실 선택 창을 띄우는 함수
    def draw(self, updateFunc1):
        self.app = Tk()
        self.app.title('Select Room')
        self.app.geometry('500x500+600+400')
        # 불러들인 강의실을 모두 버튼으로 생성하여 유저가 선택할 수 있게함.
        buttons = [Button(self.app, text = self.rooms[i], command=partial(self.Clicked, self.rooms[i], updateFunc1)
                          ).place(x=0, y=100*i, width=500, height=100) for i in range(len(self.rooms))]
        self.app.mainloop()

    def Clicked(self, room, updateFunc):
        if self.Bookmark.list.count(room) <= 0: # 선택한 강의실이 북마크 리스트에 존재하지 않을 경우
            # 북마크 리스트에 해당 강의실 추가
            self.Bookmark.list.append(room)     

        # 북마크 리스트 정렬
        self.Bookmark.list.sort()

        # 전달 받은 업데이트 함수 호출
        updateFunc()

        # 선택 창 닫기
        self.app.destroy()
