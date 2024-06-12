import sqlite3 as sql3

class TTAnalyzer():
    def __init__(self, db_path) -> None:
        #DB 경로 저장
        self.db = db_path 
        
        #결과를 리턴하기 위한 딕셔너리 키: 강의실 값:(강의, 시작, 끝)
        self.result = {}

        self.cur = None
        
    #DB 열기
    def Open_DB(self) -> bool:
            self.db = sql3.Connection(self.db)
            self.cur = self.db.cursor()
            return True
    
    #DB 내의 모든 강의실을 중복되지 않게 리턴함
    def Get_All_Room(self):
        if self.cur == None:
            self.Open_DB()

        try:
            self.cur.execute("""SELECT * FROM time""")
        except Exception as ex:
             print(ex)
        
        list = []
        for tuple in self.cur.fetchall():
            if list.count(str(tuple[0])) <= 0:
                list.append(tuple[0])

        list.sort()
        return list
    
    # 강의실, 요일, 현재시간을 이용하여 현재 강의실에서 강의가 진행 여부를 판단해
    # 강의가 진행중이라면 해당 강의 이름, 강의 시작 시간과 끝 시간 리턴
    # 비어있다면 비어있음, 이전 강의 끝 시간, 다음 강의 시작 시간 리턴
    # 해당일에 강의가 없다면 비어있음, 00:00 ~ 00:00 리턴
    def Get_timetable(self, room, weekday, time):
        if self.cur == None:
            self.Open_DB()
        
        room = (str(room).upper(), )

        # 입력한 강의실과 일치하는 행만 선택
        try:
            self.cur.execute("""SELECT * FROM time WHERE lecture_room=?""", room)
        except Exception as ex:
             print(ex)


        for tuple in self.cur.fetchall():
            if str(tuple[2]).find(weekday) != -1: # 요일이 같은 경우
                if  tuple[3] <= time and time <= tuple[4]: # 현재 시간이 강의 시작 시간과 끝 시간의 사이에 있는 경우
                    return [tuple[1], tuple[3], tuple[4], False] # 강의중으로 판단하여 리턴
                    #return 강의, 시작, 끝
        
        for tuple in self.cur.fetchall():
            if str(tuple[2]).find(weekday) != -1:
                start = 0
                for i in range(time//100): # 이전 시간으로 한 시간 단위로 변경해가며 강의 끝 시간 찾기
                    if tuple[4] >= time - i*100:
                        start = tuple[4]
                        break
                end = 0
                for i in range((1700 - time)//100): # 다음 시간으로 한 시간 단위로 변경해가며 강의 시작 시간 찾기
                    if tuple[3] <= time + i*100:
                        end = tuple[3]
                        break
                return ['비어 있음', start, end, True]
    
        return ['비어 있음', 0, 0, True]
                
                

if __name__ == '__main__':
    tta = TTAnalyzer('./TimeTable_CS.db')

    print("Get All Room")
    tta.Get_All_Room()

    print('Get_timetable')
    timetable = tta.Get_timetable("M618", '수', 14*100 + 13)
    print(timetable)