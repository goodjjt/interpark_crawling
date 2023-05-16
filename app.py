import telegram
import requests
import urllib3
import schedule
import time
from datetime import datetime
import time
from pprint import pprint
import asyncio
import psycopg2

# https 처리 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telegram
async def bot_send(msg):
    telegram_token = "5128692345:AAHkO-3JZ9tZYP2hrS5UAlnYCrO0PiO09_A"
    telegram_id = "444879086"
    bot = telegram.Bot(token = telegram_token)
    await bot.sendMessage(chat_id=telegram_id, text=msg)


# postgresSql
conn = psycopg2.connect(database="postgres",
                        host="goodjjt.iptime.org",
                        user="postgres",
                        password="wjswnsxo18!",
                        port="25432")
cursor = conn.cursor()
cursor.execute("SELECT * FROM camping_booking_info order by id")
records = cursor.fetchall()

data_array = []
url_array = []
site_gubun_array = []
payload_array = []

for row in records:
    data_array.append(row[1] + " " + row[2])
    url_array.append(row[3])
    site_gubun_array.append(row[7])
    payload_array.append(row[9])

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

print("[" + "캠핑 예약 작업 시작" + "] ")
for index, value in enumerate(data_array):
    print(value)
    print(site_gubun_array[index])
    print(payload_array[index])

def crawling():
    for index, value in enumerate(url_array):
        # 인터파크 티켓
        if site_gubun_array[index] == "interpark":
            response = requests.get(value)
            cnt = 0
            message = "[" + data_array[index] + "]" + '\n'
            if response.status_code == 200:
                jsonData = response.json()

                for data in jsonData.get("data").get("remainSeat"):
                    message = message + data.get("seatGradeName") +  " : " + str(data.get("remainCnt")) + '\n'
                    if data.get("remainCnt") > 0:
                        cnt += 1

                print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt)
                if cnt > 0:
                    asyncio.run(bot_send(message))          
            else :
                print(response.status_code)
        # 이포보 오토 캠핑장         
        if site_gubun_array[index] == "mirihae":
            response = requests.post(value, data=payload_array[index], verify=False)
            cnt = 0
            message = "[" + data_array[index] + "]" + '\n'
            if response.status_code == 200:
                jsonData = response.json()
                for data in jsonData.get('pinCategoryList')[0].get('pinList'):
                    if data.get("reserveCnt") == 0:
                        cnt += 1
                        message = message + data.get("itemNm") + ', '
                print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt)
                if cnt > 0:
                    asyncio.run(bot_send(message))    
            else :
                print(response.status_code)        

# step3.실행 주기 설정
schedule.every(10).seconds.do(crawling)
# schedule.every(30).minutes.do(message1)

while True:
    schedule.run_pending()
    time.sleep(1)            
