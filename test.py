from bs4 import BeautifulSoup
import requests

url = "https://www.ggleagues.com/dashboard/teams/870"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
s = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
print(s)
players = s.find('table',attrs={"class":"table table-hover"})
print(players)