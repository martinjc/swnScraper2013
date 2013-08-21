import urllib2
import json
import uuid

from bs4 import BeautifulSoup

root_page = "http://swnfest.com/"
venue_page = root_page + "venues/"

try:
    response = urllib2.urlopen(venue_page)
except urllib2.HTTPError, e:
    raise e
except urllib2.URLError, e:
    raise e

raw_data = response.read()

soup = BeautifulSoup(raw_data)

links = soup.select(".venue")

venues = {}

with open("venues.json") as infile:
    try:
        venues = json.load(infile)
    except ValueError, e:
        pass

for venue in links:
    link = venue.findChild("a")
    url = link.attrs["href"]
    name = venue.findChild("strong").contents[0]

    if venues.get(name, None) is None:
        if not name == "Clwb Ifor Bach":
            venues[name] = {}
            venues[name]["swn_url"] = url
            venues[name]["id"] = str(uuid.uuid4())
        else:
            venues["Clwb Ifor Bach (Downstairs)"] = {}
            venues["Clwb Ifor Bach (Downstairs)"]["swn_url"] = url
            venues["Clwb Ifor Bach (Downstairs)"]["id"] = str(uuid.uuid4())
            venues["Clwb Ifor Bach (Upstairs)"] = {}
            venues["Clwb Ifor Bach (Upstairs)"]["swn_url"] = url
            venues["Clwb Ifor Bach (Upstairs)"]["id"] = str(uuid.uuid4())
print venues

with open("venues.json", "w") as outfile:
    json.dump(venues, outfile)
