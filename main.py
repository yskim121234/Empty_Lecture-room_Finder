from tkinter import *
from TimeTable_Analyzer import TTAnalyzer as TTA
from Button import RoomButton
from Add_Bookmark import Add_Bookmark
import datetime
from functools import partial
from Search import Search
import threading

def time():
    global now
    global hour
    global minute
    global now_weekday

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    now_weekday = now.weekday()

    # 시간 설정
    menuTime.set( weekday[now_weekday]+ now.strftime(' %H:%M'))

    update()

    app.after(60 * 1000, time)


def update():
    # 북마크를 수정해야 하므로 글로벌 선언
    global bookMark

    # 초기 설정
    if len(buttons) < 1:
        buttons.append(Add_Bookmark(app, x = (len(buttons)%2)*250, y = (len(buttons)//2)*100 + 100, updateFunc1= update))
    bookMark = buttons[-1].select.Bookmark.list

    # 배치 초기화
    for b in buttons:
        b.place_forget()

    # 버튼 리스트 초기화
    buttons.clear()

    for i in range(len(bookMark)):
        if search.search.get() != '': # 검색어 입력이 있을 경우

            if bookMark[i] == search.search.get(): # 북마크 리스트에 존재하는 강의실 중 검색어와 일치하는 강의실의 정보 표시
                # 강의실 이름, 요일, 시, 분을 기반으로 강의실 시간표 검색
                d = tta.Get_timetable(bookMark[i], weekday[now_weekday], hour*100 + minute) 
                # 강의실 버튼 객체 생성
                buttons.append(RoomButton(app, room = bookMark[i],
                                           x = 0, y = 100,
                                           deleteFunc = partial(delete , bookMark[i]),
                                           lecture = d[0], 
                                           start = d[1], 
                                           end = d[2], 
                                           empty = d[3]))

        else: # 검색어 입력이 없었을 경우, 조건문 제외 위 코드와 동일
            d = tta.Get_timetable(bookMark[i], weekday[now_weekday], hour*100 + minute)

            buttons.append(RoomButton(app, room = bookMark[i],
                                       x = (i%2)*250, y = (i//2)*100 + 100,
                                       deleteFunc = partial(delete , bookMark[i]),
                                       lecture = d[0], 
                                       start = d[1], 
                                       end = d[2], 
                                       empty = d[3]))
    
    # 마지막에 북마크 추가 버튼 객체 생성
    buttons.append(Add_Bookmark(app, x = (len(buttons)%2)*250, y = (len(buttons)//2)*100 + 100, updateFunc1= update))

def Save_Bookmark():
    f = open('./Bookmark.txt', 'w')
    text = ''

    for b in bookMark:
        text += b + ','
    f.write(text[:-1])
    f.close()

def Load_Bookmark():
    f = open('./Bookmark.txt', 'r')
    line = f.readline()
    list = line.split(',')
    f.close() 
    for i in range(len(list)):
        if list[i] == '':
            del list[i]
    return list

def delete(room):
    # 해당하는 강의실 이름을 북마크 리스트에서 삭제
    buttons[-1].select.Bookmark.list.remove(room)

    # 수정된 북마크를 토대로 업데이트
    update()

# 윈도우 설정
app = Tk()
app.title("강의실 장소 검색")
app.geometry("500x700+600+300")

# 현재 시간 정보 가져오기
now = datetime.datetime.now()
hour = now.hour
minute = now.minute
# 월~일의 요일을 0~6으로 리턴함
now_weekday = now.weekday()

# 숫자를 이용하여 요일 문자 가져오기 위한 딕셔너리
weekday = {0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}

# 메뉴 {요일} {시} {분}
menuTime = StringVar()
menu = Label(app, textvariable= menuTime, fg='white', bg="blue").place(x=0, y=0, width=500, height=50)

# 검색창
search = Search(app, update)

# 강의실 정보
buttons = []
tta = TTA('./TimeTable_CS.db')

# 북마크 초기화
bookMark = []

time()
# 이벤트 루프
app.mainloop()

Save_Bookmark()