import telegram
import requests
import urllib3
import schedule
import time
from datetime import datetime
import time
from pprint import pprint

# Telegram
telegram_token = "5128692345:AAHkO-3JZ9tZYP2hrS5UAlnYCrO0PiO09_A"
telegram_id = "444879086"
bot = telegram.Bot(token = telegram_token)

url_array = [
            'https://api-ticketfront.interpark.com/v1/goods/22011899/playSeq/PlaySeq/078%2C079/REMAINSEAT'
             ]

data_array = [
            '노을진캠핑장 2022-11-10 https://tickets.interpark.com/goods/22011899'
            ]

print("[" + "interpark 예약" + "] ");
for index, value in enumerate(data_array):
    print(value)

jsonData = None
cnt = 0

def message1():
    for index, value in enumerate(url_array):
        # BeautifulSoup
        response = requests.get(value)
        cnt = 0
        message = "[" + data_array[index] + "]" + '\n'
        if response.status_code == 200:
            jsonData = response.json()
            # print(jsonData)
            for data in jsonData.get("data").get("remainSeat"):
                message = message + data.get("seatGradeName") +  " : " + str(data.get("remainCnt")) + '\n'
                if data.get("remainCnt") > 0:
                    cnt += 1
            print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt)
            # print("cnt : ", message)
            if cnt > 0:
                bot.sendMessage(chat_id=telegram_id, text=message)
                # bot_sst.sendMessage(chat_id=telegram_id_sst, text=message)
        else :
            print(response.status_code)

# step3.실행 주기 설정
schedule.every(30).seconds.do(message1)
# schedule.every(30).minutes.do(message1)

while True:
    schedule.run_pending()
    time.sleep(1)            