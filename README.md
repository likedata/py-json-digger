# Python dictionary/JSON digger

# About

The script is to help you look either for specific keys or values in multi-tier nested python dictionaries (either native or converted from JSON).

# Usage

I am using it heavily in analyzing the data retrieved from REST APIs (Google, Bing, Linkedin etc.), NoSQL dbs (MongoDB etc.), python dictionaries.

# Installation

Just clone the repository.

# Python Version

It has been developed and tested under Python 2.7.

# How to use?

```from json_digger.json_digger import JsonDigger

weather = {"coord":{"lon":-0.13,"lat":51.51},"sys":{"type":3,"id":60992,"message":0.0921,"country":"GB","sunrise":1423639268,"sunset":1423674497},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"base":"cmc stations","main":{"temp":278.05,"humidity":84,"pressure":1025.6,"temp_min":278.05,"temp_max":278.05},"wind":{"speed":2.39,"deg":122.505},"rain":{"3h":0},"clouds":{"all":80},"dt":1423646999,"id":2643743,"name":"London","cod":200}

i = JsonDigger(weather) #  initialize class instance

r_k = i.get_keys('country') #  search for key 'country'
r_v = i.get_values(278.05) #  search for value '278.05'

print r_k #  example of response: {u':sys:country': [u'GB']}
print r_v #  example of response: {u':main:temp': [278.05], u':main:temp_max': [278.05], u':main:temp_min': [278.05]}```

More in tester.py!

# Must have (if work with JSONs)

JSON module for Python (https://docs.python.org/2/library/json.html).
