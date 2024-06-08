from tkinter import *
import tkinter.messagebox  as mb

class RoomButton(LabelFrame):

    def __init__(self, root, x, y, deleteFunc, room = '', lecture = '', start = 0, end = 0, empty = False):
        # 부모 생성자를 호출해 인스턴스 초기화
        super().__init__(root, width = 250, height = 100)

        # 프레임 배치
        self.place(x=x, y=y)

        # 추후 검색을 위해 강의실 이름을 인스턴스로 저장 
        self.room = room

        # 강의실 정보 표시 라벨 생성 및 배치
        text = '%s\n%s\n%0.2d:%0.2d~%0.2d:%0.2d' %(room, lecture, start//100, start%100, end//100, end%100)
        label = Label(self, text = text)
        if empty:
            label.config(fg= 'white', bg= 'green')
        label.place(x = 0, y = 0, width = 250, height = 100)
        # 삭제 버튼 생성 및 배치
        self.icon = PhotoImage(file="./resource/Delete_Icon.png").subsample(10,10)
        Button(self, image = self.icon, command = lambda : self.Delete(deleteFunc)).place(x = 200 , y = 0, width = 50, height = 50)
        

    def Delete(self, deleteFunc):
        # 삭제 의사를 확인하기 위한 메세지 박스 생성
        answer =  mb.askyesno('삭제', "해당 항목을 삭제하시겠습니까?")

        if answer == True: # 예를 눌렀을 경우
            deleteFunc()   # 입력받은 삭제 함수 호출

if __name__ == '__main__':
    app = Tk()
    app.title("강의실 장소 검색")
    app.geometry("500x700")
    r = RoomButton(app, 0, 0, 'M610', "프기", 1400, 1500)
    app.mainloop()