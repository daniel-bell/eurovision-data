import urllib3
import json
import pycountry
from bs4 import BeautifulSoup
from datetime import datetime
import pycountry

""" Edge case countries because the Eurovision website does not
format some countries the same as pycountry """
country_mappings = {
    "Russia": "RUS",
    "Serbia and Montenegro": "SRB",
    "Yugoslavia": "YUG",
    "F.Y.R. Macedonia": "MKD",
    "Moldova": "MDA"
}


def convert_country(country_name):
    """ Converts a country name into the ISO-3166 code """
    country_name = country_name.replace("&", "and")

    # Strip leading "The" from some country names
    if country_name[:4] == "The ":
        country_name = country_name[4:]

    # Try and convert country name to alpha3 code, otherwise fall back
    # to edge case mapping
    try:
        country_code = pycountry.countries.get(name=country_name).alpha3
    except KeyError:
        country_code = country_mappings[country_name]

    return country_code

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

event_results = {}
for event in events:
    print("Parsing: http://www.eurovision.tv/" + event)
    event_req = http.request("GET", "http://www.eurovision.tv/" + event)
    event_soup = BeautifulSoup(event_req.data, "html.parser")

    # Extract list of participants
    participant_cells = event_soup.find("div", {"class": "participants"}).findAll("td", {"class": "country"})

    # Extract map of countries that are performing, including their alpha3 country code
    countries = {}
    for cell in participant_cells:
        country_code = convert_country(cell.contents[0].contents[0])
        countries[country_code] = {"performing": True, "votes": {}}

    # Extract date
    string_date = event_soup.find("p", {"class": "info"})
    event_date = datetime.strptime(string_date.contents[0], '%A %d %B %Y')

    # Extract hosting country
    event_location = event_soup.find("p", {"class": "location"}).find("a").contents[0]

    # Extract winner
    event_winner = event_soup.find("p", {"class": "winner"}).findAll("a")[1].contents[0]

    # Extract vote cells from a list of all based on title
    table_cells = event_soup.findAll("td")
    for cell in table_cells:
        # Title format is typically:
        # 3pt from Country goes to Other Country
        if "goes to" in str(cell.get("title")):
            # Extract vote details from cell title
            vote_text = cell.get("title").split(" goes to ")
            points = vote_text[0].split(" from ")[0].split("pt")[0]
            voter = vote_text[0].split(" from ")[1]
            contestant = vote_text[len(vote_text) - 1]

            if not voter == contestant and not points == "":
                # Check to see if voter is not a participant and add if they don't exist yet
                try:
                    x = countries[convert_country(contestant)]
                except KeyError:
                    countries[contestant] = {"performing": False, "votes": {}}

                countries[convert_country(contestant)]["votes"][convert_country(voter)] = int(points)

    # Build a map of the event to allow for easy JSON translation
    event_data = {"host": event_location, "date": event_date.strftime("%Y-%m-%d"), "winner": event_winner,
                  "participants": countries}
    event_results[str(event_date.year)] = event_data

# Open a file and dump the beautified JSON of the events into it
f = open("results.json", "w")
json.dump(event_results, f, sort_keys=True)