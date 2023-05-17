import requests
from bs4 import BeautifulSoup

#  User-Agent = Mozilla/5.0 (Linux; Android 8.0.0; SM-G965F Build/WHALE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Mobile Safari/537.36
response = requests.get("https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?sdate=202306", headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965F Build/WHALE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Mobile Safari/537.36'})
html = response.text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
print(soup.find_all("button", {"value":"A:2023-06-14"}))
