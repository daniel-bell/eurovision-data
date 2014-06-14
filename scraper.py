import urllib3
from bs4 import BeautifulSoup

# Download and parse main results history page
eurovision_url = "http://www.eurovision.tv/page/history/year"
http = urllib3.PoolManager()
req = http.request("GET", eurovision_url)
soup = BeautifulSoup(req.data, "html.parser")

# Extract links from only the event-entry table cells
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
    print("Parsing: http://www.eurovision.tv/" + event)
    event_req = http.request("GET", "http://www.eurovision.tv/" + event)
    event_soup = BeautifulSoup(event_req.data, "html.parser")

    # Extract vote cells from a list of all based on title
    table_cells = event_soup.findAll("td")
    votes = list()
    for cell in table_cells:
        if "goes to" in str(cell.get("title")):
            # Extract vote details from cell title
            vote_text = cell.get("title").split(" goes to ")

            # Extract points integer string and assign as 0 if blank
            points = vote_text[0].split(" from ")[0].split("pt")[0]
            points = "0" if points == "" else points

            voter = vote_text[0].split(" from ")[1]
            contestant = vote_text[len(vote_text)-1]

            if not voter == contestant:
                vote = {"voter": voter, "contestant": contestant, "points": int(points)}
                votes.append(vote)

    for vote in votes:
        print(vote)
    exit()