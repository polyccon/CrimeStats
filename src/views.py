import json
from collections import defaultdict

from flask import jsonify, request, abort, make_response, render_template
import googlemaps
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
    return render_template('home.html', name='user')


@app.route('/viewcrime', methods=['GET', 'POST'])
def viewcrime():

    keyword = request.form['keyword']
    location = request.form['location']

    try:
        gmaps = googlemaps.Client(key=read_json('params.json', 'GKEY'))

        # Geocoding an address
        geocode_result = gmaps.geocode(str(location))
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        ll = str(latitude) + ', ' + str(longitude)
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
        for key, value in d.iteritems():
            result = {
                "label": key, "value": value
                }
            results_list.append(result)

        return render_template('results.html', results=results_list)

    except Exception as e:
        print ('Error:', e)
        return 'Unable to track location, please enter a different address'
