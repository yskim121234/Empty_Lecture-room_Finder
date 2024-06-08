from selenium import webdriver
from selenium.webdriver.common.by import By
import EveryTime_Account
import time
import sqlite3
import os
import re

# 대학교 강의 시간표 DB를 만들기 위한 객체
# DB를 구성하기 위해 처음에 한 번, 추후 시간표 변경 마다 한 번씩만 돌리면 작동시키면 됨.
class TTLoader_By_EveryTime():

    def __init__(self):
        pass

    def Open(self)->bool:
        try:    # DB 생성
            self.db = sqlite3.connect('./TimeTable_CS.db')
            self.cur = self.db.cursor()

            # 해당 테이블이 존재하지 않을 경우 테이블 생성
            self.cur.execute("""CREATE TABLE IF NOT EXISTS time(
                            lecture_room TEXT,  
                            name TEXT,
                            weekday INTEGER, 
                            lecture_start INTEGER,
                            lecture_end INTEGER)""")
            return True
        except:
            print("DB Not Open")
            return False
    
    def Write(self, lecture_room, name, weekday, lecture_start, lecture_end)->bool:
        if self.db == None: # 만약 DB가 생성(오픈)되기 이전에 호출하는 경우를 대비
            print("DB is Not opened")
            return False

        # 입력받은 변수들을 각각 해당하는 열에 저장
        self.cur.execute("""INSERT INTO time (lecture_room, name, weekday, lecture_start, lecture_end) VALUES (?, ?, ?, ?, ?)""", 
                                             (lecture_room, name, weekday, lecture_start, lecture_end))
        return True
    
    def Save(self)->bool:
        if self.db == None: # DB 오픈 이전에 접근을 대비
            print("DB is not opend")
            return False
        self.db.commit() # DB 수정 사항을 적용
        return True
    
    def Close(self)->bool:
        if self.db == None: # DB 오픈 이전 접근을 대비
            print("DB is not Opend")
            return False
        
        self.db.close() # DB 닫기
        return True

    def Delete(self)->bool:
        # 현재 경로 내의 파일 리스트 리턴
        list = os.listdir('./')

        # DB를 찾았는지 판단하기 위한 bool
        finded = False
        for file in list:
            if file =='TimeTable_CS.db': # 해당 문자열과 일치하는 파일이 있을 경우
                finded = True       # 찾음 표시
                break       # 반복 중단
        
        if finded == False: # 찾지 못한 경우
            return False    # 실패를 뜻하는 False 리턴
        
        # 찾은 경우
        os.remove('./TimeTable_CS.db')  # 해당 파일 삭제
        return True

    # 따로 시간표 DB 제공처가 없으므로 '에브리 타임'을 동적 크롤링하여 DB를 생성하기 위한 함수, 본 클래스의 주 목적
    def Get_TT(self): # Get_TimeTable
        
        # 브라우저를 통해 에브리 타임 접속
        url = 'https://everytime.kr/timetable'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1) # 로딩되기 전 행동으로 에러가 발생하는 것을 방지하기 위한 기다림.

        # 에브리 타임 계정 입력, 계정 유출을 방지하기 위해 다른 파일에 매크로 설정해둠.
        user_id = EveryTime_Account.ID
        login = driver.find_element(By.NAME, 'id')
        login.clear()
        login.send_keys(user_id)

        user_pw = EveryTime_Account.PASSWORD
        login = driver.find_element(By.NAME, 'password')
        login.clear()
        login.send_keys(user_pw)

        # HTMI의 XPATH를 따라 자동으로 입력하여 에브리 타임에서 시간표를 확인 할 수 있는 페이지까지 이동
        driver.find_element(By.XPATH, """/html/body/div[1]/div/form/input""").click()
        time.sleep(2)

        driver.find_element(By.XPATH, """//*[@id="container"]/ul/li[1]""").click()
        time.sleep(2)

        driver.find_element(By.XPATH,"""//*[@id="subjects"]/div[1]/a[3]""").click()
        time.sleep(1)

        driver.find_element(By.XPATH, """//*[@id="subjectCategoryFilter"]/div/ul/li[4]""").click()
        time.sleep(1)

        driver.find_element(By.XPATH, """//*[@id="subjectCategoryFilter"]/div/ul/ul[2]/li[5]""").click()
        time.sleep(1)

        driver.find_element(By.XPATH, """//*[@id="subjectCategoryFilter"]/div/ul/ul[2]/ul[5]/li[1]""").click()
        time.sleep(3)

        # 시간표 리스트 가져오기
        table = driver.find_element(By.XPATH, """//*[@id="subjects"]/div[2]/table/tbody""")
        
        # 기존 DB 삭제
        self.Delete()

        # 새로운 DB 생성
        self.Open()

        # 각 시간표마다 반복
        for tr in table.find_elements(By.TAG_NAME, "tr"):

            td = tr.find_elements(By.TAG_NAME, 'td')
            
            # 필요한 정보를 변수에 저장, 직관성을 위함
            room = td[4].text
            when = td[3].text
            subject = td[1].text
            
            # 외부 활동 제외
            if room == 'X016':
                continue
            
            # 강의 시간이 1,2,3 | 1-3 등 일관되지 않은 형태이기 때문에 정규화 시켜줌
            when = re.sub("-|,",'~', when)
            # 1,2,3 -> 1~2~3이 되었을 때 1~3으로 만들어주기 위함
            when = re.sub("~\d~|~\d\w~",'~',when)
            
            # 여러 강의실을 이용하는 강의의 경우 M610/M615등으로 표기되어 불편이 생김
            # 이러한 부분까지 처리하기엔 소요되는 시간에 비해 리턴이 적기 때문에 작업을 생략하기 위한 컷처리
            if room.find('/') != -1:
                room = room[0:room.find('/')]

            
            if when.find('/') != -1: # 강의시간이 월 1B~2B/목 5~6 등 하나의 행에 여러 시간이 표시된 경우
                # 강의시간을 /를 기준으로 둘로 나눔
                a, b = when.split('/')
                
                # 각 문자열의 첫 인덱스는 요일이므로 요일과 시간을 따로 저장
                a_weekday = a[0]
                a = a[1:]
                # 1A~3B등 직관적이지 않은 시간 표시를 24시간 체계로 변환
                a = self.Normalize_Time(a)

                b_weekday = b[0]
                b = b[1:]
                b = self.Normalize_Time(b)
                
                # 다듬어진 정보를 DB에 저장
                self.Write(room, subject, a_weekday, a[0], a[1])
                self.Write(room, subject, b_weekday, b[0], b[1])
            else: # 강의시간이 하나인 경우
                # 강의시간을 둘로 나누는 것 제외 위와 같음
                weekday = when[0]
                when = when[1:]
                when = self.Normalize_Time(when)
                self.Write(room, subject, weekday, when[0], when[1])

        self.Save() # 저장
        self.Close() # 닫기
        return True
    
    def Normalize_Time(self, time):
        # 시 정보는 정수, 분 정보는 문자로 표현되므로 정수만 추출하여 저장
        # 앞서 정규화를 통해 정수는 단 두개뿐임. 즉 리턴되는 리스트의 0번 인덱스는 시작, 1번 인덱스는 끝.
        hour = re.findall(r'\d', time)

        # 현재 시간과 비교가 필요하므로 계산 가능한 숫자의 형태로 저장되어야함.
        # 다만 60분법을 사용하면 표현과 계산이 복잡해짐
        # 그러므로 24시간 체계를 4자릿수 숫자로 표현, 앞의 두자리는 시, 뒤의 두자리는 분을 표현하여 간소화.
        # 시가을 다시 얻어올 때에는 시 = 값//100, 분 = 값%100을 통해 얻어올 수 있음
        for i in range(len(hour)):
            hour[i] = (int(hour[i])+8)*100

        # A와 B를 통해 분 단위의 시간을 표시하지만 이는 한 때를 가르키는 것이 아닌, 30분 범위를 나타냄. A = 00분 ~ 30분
        # 즉 시작과 끝의 A, B는 서로 다른 분으로 표현해야함. 1B ~ 2B -> 9:30 ~ 11:00 처럼 같은 B지만 다르게 표기해야함
        minute = re.findall(r'[^\d | ^~]', time)
        time = []
        if len(minute) >= 2: # A, B를 이용한 분 단위 표시가 되어 있는 경우
            for i in range(2):
                if minute[i] == 'A':
                    if i == 0:
                        time.append(hour[0])
                    else:
                        time.append(hour[1] + 30)
                elif minute[i] == 'B':
                    if i == 0:
                        time.append(hour[0] + 30)
                    else:
                        time.append(hour[1]+ 100)
        else:
            if len(hour) < 2: # 시간이 1 범위가 지정되지 않고 한 시간만을 이야기하는 경우 해당 시간을 시작으로 한 시간 동안 진행됨을 의미함
                time = [hour[0], hour[0]+100] # 1을 09:00이 아닌 09:00~10:00으로 표현
            else: # 1~2와 같은 평범한 경우 또한 09:00~10:00이 아닌 각각 1 = 09:00~10:00, 2= 10:00~11:00을 뜻하므로 -> 09:00~11:00
                for i in range(2):
                    time.append(hour[i] + i) # 시작점의 시간은 그대로, 끝점의 시간은 +1
        return time # 정리된 시간을 리턴

if __name__ == '__main__':
    ttloader = TTLoader_By_EveryTime()
    ttloader.Get_TT()
    