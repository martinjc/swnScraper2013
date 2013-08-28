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

        #if venue_data.get("foursquare_id", None) is None:

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
        print data
        v = data['response']['venues'][0]
        venue_data['foursquare_id'] = v['id']
        venue_data['name'] = v['name']
        venue_data['lat'] = v['location']['lat']
        venue_data['lng'] = v['location']['lng']
        if v['location'].get("postalCode", None) is not None:
            venue_data['postalCode'] = v["location"]["postalCode"]
        else:
            venue_data['postalCode'] = ""
        if v["location"].get("address", None) is not None:
            venue_data["adline1"] = v["location"]["address"]
        else:
            venue_data["adline1"] = ""
        if v["location"].get("crossStreet", None) is not None:
            venue_data["adline2"] = v["location"]["crossStreet"]
        else:
            venue_data["adline2"] = ""      


with open("venues.json", "w") as outfile:
    json.dump(venues, outfile)