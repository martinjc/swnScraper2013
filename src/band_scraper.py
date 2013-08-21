import urllib2
import json
import uuid

from bs4 import BeautifulSoup

root_page = "http://swnfest.com/"
lineup_page = root_page + "lineup/"

try:
    response = urllib2.urlopen(lineup_page)
except urllib2.HTTPError, e:
    raise e
except urllib2.URLError, e:
    raise e

raw_data = response.read()

soup = BeautifulSoup(raw_data)

links = soup.select(".artist-listing h5 a")

artists = {}

with open("bands.json") as infile:
    try:
        artists = json.load(infile)
    except ValueError, e:
        pass

for link in links:
    url =  link.attrs["href"]
    artist = link.contents[0]

    if artists.get("artist", None) is None:

        artists[artist] = {}
        artists[artist]["swn_url"] = url


for artist, data in artists.iteritems():
    try:
        response = urllib2.urlopen(data["swn_url"])
    except urllib2.HTTPError, e:
        raise e
    except urllib2.URLError, e:
        raise e

    raw_data = response.read()

    soup = BeautifulSoup(raw_data)

    links = soup.select(".outlinks li")

    for link in links:
        source = link.attrs["class"][0]
        source_url = link.findChild("a").attrs["href"]

        data[source] = source_url

    if data.get("id", None) is None:
        artist_data["id"] = str(uuid.uuid4())

with open("bands.json", "w") as outfile:
    json.dump(artists, outfile)