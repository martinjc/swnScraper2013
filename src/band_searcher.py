import urllib2
import urllib
import json

from _credentials import last_fm_api_key

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

        spotify_root_url = "http://ws.spotify.com/search/1/artist.json?"

        spotify_url =  spotify_root_url + urllib.urlencode(params)

        data = retrieve_json_data(spotify_url)

        if data.get("artists", None) is not None:
            if len(data["artists"]) > 0:
                artist_id = data["artists"][0]["href"].lstrip("spotify:artist:")
                artist_data["spotify_id"] = data["artists"][0]["href"]
                artist_data["spotify_url"] = "http://open.spotify.com/artist/" + artist_id

    if artist_data.get("last_fm_url", None) is None:

        params = {
            "artist": artist.encode("utf-8"),
            "api_key": last_fm_api_key,
            "method": "artist.getinfo",
            "format": "json"
        }

        last_fm_url = "http://ws.audioscrobbler.com/2.0/?" + urllib.urlencode(params)

        data = retrieve_json_data(last_fm_url)

        if data.get("artist", None) is not None:
            if data["artist"].get("url", None) is not None:
                artist_data["last_fm_url"] = data["artist"]["url"]

        params = {
            "artist": artist.encode("utf-8"),
            "api_key": last_fm_api_key,
            "method": "artist.gettoptags",
            "format": "json"
        }

        last_fm_url = "http://ws.audioscrobbler.com/2.0/?" + urllib.urlencode(params)

        data = retrieve_json_data(last_fm_url)

        if data.get("toptags", None) is not None:
            
            artist_data["tags"] = {}

            if data["toptags"].get("tag", None) is not None:
                tags = data["toptags"]["tag"]
                if type(tags) == type([]):
                    for tag in tags:
                        name = tag["name"].encode('utf-8')
                        count = 1 if int(tag["count"]) == 0 else int(tag["count"])
                        artist_data["tags"][name] = count
                else:
                    name = tags["name"].encode('utf-8')
                    count = 1 if int(tags["count"]) == 0 else int(tags["count"])
                    artist_data["tags"][name] = count

with open("bands.json", "w") as outfile:
    json.dump(artists, outfile)