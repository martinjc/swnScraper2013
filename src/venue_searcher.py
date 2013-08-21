import urllib2
import urllib
import json

from _credentials import foursquare_client_secret, foursquare_client_id

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


venues = {}

with open("venues.json") as infile:
    venues = json.load(infile)

    foursquare_root_url = "https://api.foursquare.com/v2/venues/search?"
    
    for venue, venue_data in venues.iteritems():
        print venue

        if venue_data.get("foursquare_id", None) is None:

            params = {
                    "ll" : "51.48,-3.18",
                    "query": "%s" % (venue.encode('utf-8')),
                    "intent": "checkin",
                    "v" : 20130821,
                    "client_id" : foursquare_client_id,
                    "client_secret" : foursquare_client_secret
            }

            search_url = foursquare_root_url + urllib.urlencode(params)

            data = retrieve_json_data(search_url)

            venue_data['foursquare_id'] = data['response']['venues'][0]['id']
            venue_data['name'] = data['response']['venues'][0]['name']
            venue_data['lat'] = data['response']['venues'][0]['location']['lat']
            venue_data['lng'] = data['response']['venues'][0]['location']['lng']

with open("venues.json", "w") as outfile:
    json.dump(venues, outfile)