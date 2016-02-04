#!/usr/bin/python
# -*- coding: utf-8 -*-

from json_digger.json_digger import JsonDigger

#  Function to retrieve JSON
def api_request_sender(url):

    try:
        import requests
        data_output = requests.get(url)

    except:
        # Python 2 only
        import urllib2
        data_output = urllib2.urlopen(url)

    return data_output

url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk' #  sample JSON from RESTful API

# retrieved_json_net = api_request_sender(url) #  get the response

#  On 11 Feb 2015 JSON was as below:
retrieved_json_net = {"coord":{"lon":-0.13,"lat":51.51},"sys":{"type":3,"id":60992,"message":0.0921,"country":"GB","sunrise":1423639268,"sunset":1423674497},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"base":"cmc stations","main":{"temp":278.05,"humidity":84,"pressure":1025.6,"temp_min":278.05,"temp_max":278.05},"wind":{"speed":2.39,"deg":122.505},"rain":{"3h":0},"clouds":{"all":80},"dt":1423646999,"id":2643743,"name":"London","cod":200}

i = JsonDigger(retrieved_json_net) #  initialize class instance

r_k = i.get_keys('country') #  search for key 'country'
r_v = i.get_values(278.05) #  search for value '278.05'

assert r_k == {u':sys:country': [u'GB']}
assert r_v == {u':main:temp': [278.05], u':main:temp_max': [278.05], u':main:temp_min': [278.05]}

#  alternative call - directly the function inside class
assert JsonDigger.f_dig_for_keys(retrieved_json_net, 'country') == {u':sys:country': [u'GB']}
assert JsonDigger.f_dig_for_values(retrieved_json_net, 278.05) == {u':main:temp': [278.05], u':main:temp_max': [278.05], u':main:temp_min': [278.05]}
