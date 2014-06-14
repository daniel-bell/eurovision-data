import urllib3
from bs4 import BeautifulSoup

eurovision_url = "http://www.eurovision.tv/page/history/year"
http = urllib3.PoolManager()

req = http.request("GET", eurovision_url)
soup = BeautifulSoup(req.data)
links = soup.findAll("a")

for link in links:
    print(link)