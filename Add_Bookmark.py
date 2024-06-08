from tkinter import *
from Select_room import Select_room

class Add_Bookmark():

    def __init__(self, root, x, y, updateFunc1):
    
        self.root = root
        # 이미지 불러온 후 사이즈 조정 및 저장
        self.icon = PhotoImage(file="./resource/Plus_Icon.png").subsample(2,2)

        # 강의실 선택을 위한 객체
        self.select = Select_room()

        # 입력받은 업데이트 함수를 바인딩한 버튼 생성
        self.button = Button(root, command= lambda : self.Select(updateFunc1) ,image=self.icon)
        self.button.place(x = x, y = y, width = 250, height = 100)

    def Select(self, updateFunc1):
        # Select_room의 창을 띄우는 함수
        self.select.draw(updateFunc1)

    def place_forget(self):
        # 본 클래스가 widget을 부모로 가지지 않아 배치 초기화 함수가 존재하지 않음.
        # 하지만 widget을 부모로 가진 Button을 소유하고 있으므로 배치 초기화 명령을 전달할 필요가 있음.
        self.button.place_forget()

if __name__ == '__main__':
    #윈도우 생성
    app = Tk()
    app.title("plus button")
    app.geometry('250x200')

    bm = Add_Bookmark(app, 0, 0)
    s = StringVar()
    
    Label(app, textvariable=s, bg='blue').place(x=0, y=100, width=250, height=100)
    app.mainloop()

    # 누르면 리스트 박스 나와서 강의실 선택하고 그거 리턴
    #끝