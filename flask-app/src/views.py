import json
from collections import defaultdict

from flask import jsonify, request, abort, make_response, render_template, redirect
import requests

from src.core import app
from readfile import read_json


def _parse_request_body():
    """Extract data type from request body."""
    request_body = request.get_json()
    try:
        id_ = request_body['id']
        items = request_body['items']

    except KeyError:
        # Missing necessary fields.
        response_body = {
            'error':
            "'id', 'items' key in request body"
        }
        abort(make_response(jsonify(response_body), 400))
    return id_, items


@app.route('/healthz', methods=['GET'])
def healthz():
    return ('', 200)


@app.route("/")
def hello():
    return render_template('home.html')


@app.route("/home")
def home():
    return redirect("/")


def get_data(location):
    url_postcode = "http://api.postcodes.io/postcodes/"+location
    resp_postcode = requests.get(url=url_postcode)
    ll = json.loads(resp_postcode.text)['result']
    latitude = ll['latitude']
    longitude = ll['longitude']
    url = 'https://data.police.uk/api/crimes-street/all-crime?'
    params = dict(
        lat=latitude,
        lng=longitude
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    d = defaultdict(dict)
    for item in data:
        if not d.get(item['category']):
            d[item['category']] = 1
        else:
            d[item['category']] += 1

    results_list = []
    for key, value in d.items():
        result = {
            'label': key, 'value': value
            }
        results_list.append(result)
    return results_list


@app.route('/data/<location>')
def data(location):
    return jsonify(get_data(location))


@app.route('/viewcrime', methods=['GET', 'POST'])
def viewcrime():
    postcode = request.form['postcode']
    return render_template('results.html', location=postcode)
