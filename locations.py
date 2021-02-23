"""This module gets json file from twitter and extracts information
of users' friends usernames and locations"""
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
access_token = "AAAAAAAAAAAAAAAAAAAAACl6MwEAAAAAbBTTF5RTQiaUrsj5M76yX0vpvW4%3DgWQVEVdOHRkuZr4gbek3Q1EOxHV9NFabwIB0gOBWBe3EV5CZlI"


def get_friends_locations(screen_name, bearer_token):
    """
    Gets json file from twitter using requests
    and returns locations and usernames of the account of screen_name
    :param screen_name: twitter username
    :param bearer_token: API twitter bearer token
    :return: dictionary, key is username, value is location
    """
    locations = {}
    base_url = "https://api.twitter.com/"
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
        }
    search_params = {
        'screen_name': '@'+screen_name,
        'count': 30
    }

    search_url = '{}1.1/friends/list.json'.format(base_url)
    response = requests.get(search_url, headers=search_headers, params=search_params)
    json_response = response.json()
    for user in json_response['users']:
        friend_name = user['name']
        friend_location = user['location']
        if friend_location and friend_name:
            locations[friend_name] = friend_location
    return locations


def followers_coordinates(locations):
    """
    Returns users' coordinates according to locations
    :param locations: dictionary, key is username, value is location
    :return: dictionary, key is username, value is coordinates
    """
    new_locations = {}
    geolocator = Nominatim(user_agent="Movies'_Places")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    for place in locations.keys():
        try:
            location = geolocator.geocode(place[-1])
            coordinates = [location.latitude, location.longitude]
            locations[place] = coordinates
        except GeocoderUnavailable:
            pass
        except AttributeError:
            pass
    for key in locations:
        if isinstance(locations[key], list):
            new_locations[key] = locations[key]
    return new_locations


def create_map(locations):
    """
    Creates html map with followers of user
    :param locations: dictionary, key is username, value is coordinates
    :return: nothing
    """
    raw_map = folium.Map()
    followers_map = folium.FeatureGroup(name="Markers")
    for key in locations:
        user_name = key
        location = locations[key]
        folium.Marker(location=location, popup=user_name).add_to(followers_map)
    raw_map.add_child(followers_map)
    raw_map.add_child(folium.LayerControl())
    raw_map.save("templates/followers_map.html")


create_map(followers_coordinates(get_friends_locations('kvestrelanda', access_token)))
