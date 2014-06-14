import urllib3
from bs4 import BeautifulSoup

# Download and parse main results history page
eurovision_url = "http://www.eurovision.tv/page/history/year"
http = urllib3.PoolManager()
req = http.request("GET", eurovision_url)
soup = BeautifulSoup(req.data, "html.parser")

# Extract links from only the history-by-year div
cells = soup.findAll("td", {"class": "event-entry"})
links = list()
for cell in cells:
    links.append(cell.find("a"))

# Extract a links into a set to remove any duplicates
events = set()
for link in links:
    # Substring use to prevent extraction of unwanted links
    if "/page/history/by-year/contest?event=" in link.get("href"):
        events.add(link.get("href"))

print(str(len(events)) + " events found")

for event in events:
    print(event)