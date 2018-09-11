import json


def read_json(filename, key):
    with open(filename, 'r') as f:
        json_dict = json.load(f)

    for item in json_dict:
        return item['config'][key]
