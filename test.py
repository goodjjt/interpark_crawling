import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib3
import urllib
import time

search_dt = datetime.fromisoformat("2023-05-28") + timedelta(hours=-9)
search_dt_convert = int( ( search_dt - datetime.utcfromtimestamp(0) ).total_seconds() * 1000.0 )
print(search_dt_convert)

# https 처리 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#  User-Agent = Mozilla/5.0 (Linux; Android 8.0.0; SM-G965F Build/WHALE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Mobile Safari/537.36
response = requests.get("https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?sdate=202306", headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965F Build/WHALE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Mobile Safari/537.36'})
html = response.text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
area = ['A', 'B', 'C', 'D', 'E']
for data in area:
    strTemp = data + ":2023-06-08"
    print(strTemp)
    print(soup.find_all("button", {"value":strTemp}))
print(soup.find_all("button", {"value":strTemp}))

# url = "https://api.camfit.co.kr/v1/camps/zones/640eb93732fea4001ee164e6?id=640eb93732fea4001ee164e6&adult=2&teen=0&child=1&startTimestamp=1685804400000&endTimestamp=1685977200000&limit=4&skip=0"
# headers = {'Origin': 'www.camfit.co.kr',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#            }
# response = requests.get(url, headers=headers)
# jsonData = response.json()
# print(jsonData[1].get(""))
# for data in jsonData:
#     print(data.get("unavailableReason"))
# # print(soup.find_all("button", {"value":"A:2023-06-03"}))


# print(urllib.parse.quote("원주키즈캠핑장"))

# reqUrl = "https://api.camfit.co.kr/v2/search?search=" + urllib.parse.quote("산솔오토캠핑장") + "&types=autoCamping&checkInTimestamp=1685718000000&checkoutTimestamp=1685890800000&skip=0&limit=10"

# headersList = {
#  "Accept": "*/*",
#  "User-Agent": "Thunder Client (https://www.thunderclient.com)",
#  "Origin": "www.camfit.co.kr" 
# }

# payload = ""

# response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
# jsonData = response.json()
# print("캠프99")
# for data in jsonData:
#     print(data.get("name"), " : ", data.get("isAvailable"))


#https://www.camfit.co.kr/camp/6333f06b2c60d8001e8b45e3