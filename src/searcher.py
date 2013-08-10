import urllib2
import urllib
import json

def retrieve_json_data(url):

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        raise e
    except urllib2.URLError, e:
        raise e

    raw_data = response.read()
    data = json.loads(raw_data)

    return data



artists = {}

with open("bands.json") as infile:
    artists = json.load(infile)


for artist, artist_data in artists.iteritems():

    if artist_data.get("spotify_url", None) is None:
        params = {
            "q" : "artist:" + artist.encode("utf-8")
        }

        spotify_url = "http://ws.spotify.com/search/1/artist.json?" + urllib.urlencode(params)

        data = retrieve_json_data(spotify_url)

        if data.get("artists", None) is not None:
            if len(data["artists"]) > 0:
                print data["artists"][0]
                artist_data["spotify_url"] = data["artists"][0]["href"]
                print artist_data["spotify_url"]

with open("bands.json", "w") as outfile:
    json.dump(artists, outfile)