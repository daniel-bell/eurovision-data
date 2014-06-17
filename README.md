eurovision-data
===============

A web scraper of the Eurovision Song Contest [Results Website](http://www.eurovision.tv/page/history/year) written in Python and [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/).

## Data

results.json includes all valid Eurovision events extracted on `2014-06-15`

The data included is as follows:

* Contest date
* Host country
* Winning country
* List of participant Countries
    * Whether they are performing
    * The points they've been awarded by other countries

## Requirements

None if you wish to use the JSON. If you wish to extract the data yourself then the following Python packages need to be installed:

* [urllib3](https://pypi.python.org/pypi/urllib3)
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/)