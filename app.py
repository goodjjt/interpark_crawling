import telegram
import requests
import urllib3
import schedule
import time
from datetime import datetime
import time
from pprint import pprint
import asyncio
import psycopg2.extras
from bs4 import BeautifulSoup

# https 처리 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telegram
async def bot_send(msg):
    telegram_token = "5128692345:AAHkO-3JZ9tZYP2hrS5UAlnYCrO0PiO09_A"
    telegram_id = "444879086"
    bot = telegram.Bot(token = telegram_token)
    await bot.sendMessage(chat_id=telegram_id, text=msg)

# Telegram
async def bot_send_eo(msg):
    telegram_token = "6435631419:AAHlNw7alHuvilFa4rQmSH27teXUZRxWq_E"
    telegram_id = "6070929358"
    bot = telegram.Bot(token = telegram_token)
    await bot.sendMessage(chat_id=telegram_id, text=msg)


# postgresSql
conn = psycopg2.connect(database="postgres",
                        host="goodjjt.iptime.org",
                        user="postgres",
                        password="wjswnsxo18!",
                        port="25432")
cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
cursor.execute("select * from camping_booking_info where 1 = 1 order by id")
records = cursor.fetchall()

print("[" + "캠핑 예약 작업 시작" + "] ")
for index, value in enumerate(records):
    if value['use_yn'] == "Y":
        print(value['camping_site_name'] + " " + value['site_url'])

# data_array = []
# url_array = []
# site_gubun_array = []
# payload_array = []

# for row in records:
#     data_array.append(row['camping_site_name'] + " " + row['site_url'])
#     url_array.append(row['request_url'])
#     site_gubun_array.append(row['site_gubun'])
#     payload_array.append(row['payload'])

# url_array = [
#             'https://api-ticketfront.interpark.com/v1/goods/22002652/playSeq/PlaySeq/256/REMAINSEAT',
#             'https://api-ticketfront.interpark.com/v1/goods/22011899/playSeq/PlaySeq/143/REMAINSEAT',
#             'https://api-ticketfront.interpark.com/v1/goods/22005895/playSeq/PlaySeq/317/REMAINSEAT',
#             'https://api-ticketfront.interpark.com/v1/goods/21012652/playSeq/PlaySeq/503/REMAINSEAT'
#              ]

# data_array = [
#             '노을 캠핑장 2023-05-19 https://tickets.interpark.com/goods/22002652',
#             '노을진 캠핑장 2023-05-19 https://tickets.interpark.com/goods/22011899',
#             '킨텍스 캠핑장 2023-05-19 https://tickets.interpark.com/goods/22005895',
#             '천왕산 캠핑장 2023-05-19 https://tickets.interpark.com/goods/21012652'
#             ]



def crawling():
    cursor.execute("select * from camping_booking_info where 1 = 1 order by id")
    records = cursor.fetchall()
    for index, value in enumerate(records):
        if value['use_yn'] == "Y":
            # 맑음터공원캠핑장
            # if value['site_gubun'] == "forest.maketicket":
            #     response = requests.get(value['request_url'], data=value['payload'])
            #     cnt = 0
            #     message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
            #     if response.status_code == 200:
            #         htmlData = response.text
            #         soup = BeautifulData, 'html.parser')
            #         array_temp = ['A', 'B', 'C', 'D', 'E']
            #         for data in array_temp:
            #             soup.find_all("button", {"value":"A:2023-06-08"})
            #             message = message + data.get("name") +  " : " + data.get("isAvailable") + '\n'
            #             if data.get("isAvailable") == "True":
            #                 cnt += 1
 
            #         print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
            #         if cnt > 0:
            #             asyncio.run(bot_send(message))          
            #     else :
            #         print(response.status_code)
            # 연곡 솔향기
            if value['site_gubun'] == "camping.gtdc":
                response = requests.get(value['request_url'], data=value['payload'],  headers=value['headers'])
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    htmlData = response.text
                    soup = BeautifulSoup(htmlData, 'html.parser')
                    array_temp = ['A', 'B', 'C', 'D', 'E']
                    for data in array_temp:
                        soup.find_all("button", {"value":"A:2023-06-08"})
                        message = message + data.get("name") +  " : " + data.get("isAvailable") + '\n'
                        if data.get("isAvailable") == "True":
                            cnt += 1

                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message))          
                else :
                    print(response.status_code)
            # 캠핏
            if value['site_gubun'] == "camfit":
                response = requests.get(value['request_url'], data=value['payload'], headers={'User-Agent':'Mozilla/5.0', 'Origin': 'www.camfit.co.kr'})
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    jsonData = response.json()
            
                    for data in jsonData:
                        message = message + (data.get("name") +  " : " + str(data.get("isAvailable")) + '\n')
                        if data.get("isAvailable") == True:
                            cnt += 1

                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message))          
                else :
                    print(response.status_code)
            # 인터파크 티켓
            if value['site_gubun'] == "interpark":
                response = requests.get(value['request_url'], headers={'User-Agent':'Mozilla/5.0'})
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    jsonData = response.json()

                    for data in jsonData.get("data").get("remainSeat"):
                        message = message + data.get("seatGradeName") +  " : " + str(data.get("remainCnt")) + '\n'
                        if data.get("remainCnt") > 0:
                            cnt += 1

                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message)) 
                        asyncio.run(bot_send_eo(message))         
                else :
                    print(response.status_code)
            # 이포보 오토 캠핑장         
            if value['site_gubun'] == "mirihae":
                response = requests.post(value['request_url'], data=value['payload'], verify=False)
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    jsonData = response.json()
                
                    for data in jsonData.get('pinCategoryList')[0].get('pinList'):
                        if data.get("reserveCnt") == 0:
                            cnt += 1
                            message = message + data.get("itemNm") + ', '
                    
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message))    
                else :
                    print(response.status_code)     
            # 난지 캠핑장         
            if value['site_gubun'] == "yeyak.seoul":
                response = requests.post(value['request_url'], data=value['payload'], verify=False, headers={'User-Agent':'Mozilla/5.0'})
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    jsonData = response.json()

                    for data in jsonData.get('resultListDays'):
                        if data.get("SVC_RESVE_CODE") == "Y":
                            if data.get("YMD") == "20230304":
                                cnt += 1
                                message = message + data.get("YMD")

                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message))   
                        asyncio.run(bot_send_eo(message))       
                else :
                    print(response.status_code)      
            # 임진각 평화누리 캠핑장         
            if value['site_gubun'] == "imjingakcamping":
                response = requests.post(value['request_url'])
                cnt = 0
                message = "[" + value['camping_site_name'] + " " + value['site_url'] + "]" + '\n'
                if response.status_code == 200:
                    jsonData = response.json()

                    if jsonData.get("result").items() is not None:
                        for key, item in jsonData.get("result").items():
                            if item == "0":
                                # 평화캠핑존
                                if key.startswith("ph"):
                                    # print("평화캠핑존", " : ", key, " : ", value)
                                    message = message + "평화캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                                    cnt += 1
                                # 힐링캠핑존
                                if key.startswith("hl"):
                                    message = message + "힐링캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                                    cnt += 1
                                # 누리캠핑존
                                if key.startswith("nr"):
                                    message = message + "누리캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                                    cnt += 1
                                # 에코캠핑존
                                if key.startswith("ec"):
                                    message = message + "에코캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                                    cnt += 1
                                
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt, ":", value['camping_site_name'])
                    if cnt > 0:
                        asyncio.run(bot_send(message))    
                        asyncio.run(bot_send_eo(message))   
                else :
                    print(response.status_code)      

# step3.실행 주기 설정
schedule.every(10).seconds.do(crawling)
# schedule.every(30).minutes.do(message1)

while True:
    schedule.run_pending()
    time.sleep(1)            
