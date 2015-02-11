#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The script is to make it easier to dig through multi-tier nested dictionaries and look for specific keys or values therein.

It returns search results as a dictionary, where:
    Key represents: exact path to the searched key/value - built based on concatenation of processed keys e.g. 'Key1:Key4:Key100'
    Value represents: list of value/s that are searched for or are under given key/s that are searched for e.g. [value1,value4]

The idea for path as a output dictionary key is to be able to easy trace the searched keys/values.

Example no 1:
Search for key: 'Key100'
Result: {Key1:Key4:Key100: [value1,value4], Key1:Key100: [value99]}
    where it means:
        You were looking for key named 'Key100' and inside your dictionary there are two such keys and they have been assigned with different values.

Example no 2:
Search for value: 'value4'
Result: {Key1:Key4:Key199: [[value1,value4],[value4]], Key1:Key100: [value4]}
    where it means:
        You were looking for 'value4' and inside your dictionary there are two such keys that hold such value.
"""


import json


class JsonDiggerFunctions(object):

    @staticmethod
    def json_converter(json_in_dict_out):

        if not isinstance(json_in_dict_out,dict):

            try:
                json_in_dict_out = json_in_dict_out.json()

            except:
                try:
                    json_in_dict_out = json.load(json_in_dict_out)

                except:
                    raise RuntimeError('Please ensure the input parameter is JSON or Python dict!')

        return json_in_dict_out

    @staticmethod
    def f_dig_for_keys(dictionary, search_key, dict_path='', results_key={}, dict_level=0, previous_lvl_key=[]):

        dictionary = JsonDiggerFunctions.json_converter(dictionary) #  convert JSON to py dict

        search_key = str(search_key) #  convert variable type to str

        if dict_level == 0:
            results_key.clear()  # clear output dict

        dict_level += 1  # set current dict depth level

        for key in dictionary:  # iterate through dictionary

            if previous_lvl_key != [] and dict_level - previous_lvl_key[0] == 1:  # setting dict path
                dict_path = dict_path + ':' + previous_lvl_key[1]

            previous_lvl_key = [dict_level, key]  # get the previous key name and depth level

            # convert all dict variable types to str
            if not (isinstance(key, dict) or isinstance(key, list) or isinstance(key, tuple)):
                key = str(key)

            if key == search_key:

                dict_path = dict_path + ':' + str(key)  # setting dict path

                if dict_path in results_key.keys():
                    results_key[dict_path] = results_key[dict_path] + [dictionary[key]]  # append list of keys

                else:
                    results_key[dict_path] = [dictionary[key]]  # append key

                dict_path = dict_path[:dict_path.rfind(':')]  # remove last key from dict path

            elif isinstance(dictionary[key], dict):
                    # call function in recursive mode
                    JsonDiggerFunctions.f_dig_for_keys(dictionary[key], search_key=search_key, dict_path=dict_path,
                                         dict_level=dict_level, previous_lvl_key=previous_lvl_key)

            elif isinstance(dictionary[key], list) or isinstance(dictionary[key], tuple):

                for element in dictionary[key]:

                    if isinstance(element, dict):
                        # call function in recursive mode
                        JsonDiggerFunctions.f_dig_for_keys(element, search_key=search_key, dict_path=dict_path,
                                             dict_level=dict_level, previous_lvl_key=previous_lvl_key)

        return results_key

    @staticmethod
    def f_dig_for_values(dictionary, search_key, dict_path='', results_value={}, dict_level=0, previous_lvl_key=[]):

        dictionary = JsonDiggerFunctions.json_converter(dictionary) #  convert JSON to py dict

        search_key = str(search_key) #  convert variable type to str

        if dict_level == 0:
            results_value.clear()  # clear output dict

        dict_level += 1  # set current dict depth level

        for key in dictionary:  # iterate through dictionary

            if previous_lvl_key != [] and dict_level - previous_lvl_key[0] == 1:
                dict_path = dict_path + ':' + previous_lvl_key[1]  # setting dict path

            previous_lvl_key = [dict_level, key]  # get the previous key name and depth level

            # solve conflicts when automatic encoding to ASCII
            if isinstance(dictionary[key],unicode):
                _str = dictionary[key].encode('utf-8')
            else:
                _str = dictionary[key]

            # convert all dict variable types to str
            if not (isinstance(_str, dict) or isinstance(_str, list) or isinstance(_str, tuple)):
                _str = str(_str)

            if str(_str).find(search_key) != -1 and isinstance(_str, str):

                dict_path = dict_path + ':' + str(key)  # setting dict path

                if dict_path in results_value.keys():
                    results_value[dict_path] = results_value[dict_path] + [dictionary[key]]  # append list of values
                else:
                    results_value[dict_path] = [dictionary[key]]  # append value

                dict_path = dict_path[:dict_path.rfind(':')]  # remove last key from dict path

            elif isinstance(dictionary[key], dict):
                # call function in recursive mode
                JsonDiggerFunctions.f_dig_for_values(dictionary[key], search_key=search_key, dict_path=dict_path,
                                       dict_level=dict_level, previous_lvl_key=previous_lvl_key)

            elif isinstance(dictionary[key], list) or isinstance(dictionary[key], tuple):

                for element in dictionary[key]:

                    if isinstance(element, int):
                        element = str(element)

                    if isinstance(element, dict):
                        # call function in recursive mode
                        JsonDiggerFunctions.f_dig_for_values(element, search_key=search_key, dict_path=dict_path,
                                               dict_level=dict_level, previous_lvl_key=previous_lvl_key)

                    elif str(element).find(search_key) != -1 and isinstance(element, str):

                        if dict_path in results_value.keys():
                            results_value[dict_path] = results_value[dict_path] + [element]  # append list of values
                        else:
                            results_value[dict_path] = [element]  # append value

        return results_value


class JsonDigger(JsonDiggerFunctions):

    def __init__(self, dictionary, keyword=''):
        self.dictionary = dictionary
        self.keyword = keyword

    def get_keys(self, keyword):
        self.keyword = keyword
        try:
            return self.f_dig_for_keys(self.dictionary, self.keyword)
        except Exception, Error:
            print Error

    def get_values(self, keyword):
        self.keyword = keyword
        try:
            return self.f_dig_for_values(self.dictionary, self.keyword)
        except Exception, Error:
            print Error