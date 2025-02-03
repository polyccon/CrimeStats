from flask import jsonify, request, abort, make_response, render_template, redirect

from src.core import app

from src.data.convert_data import get_data

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


@app.route('/data/<location>')
def data(location):
    return jsonify(get_data(location))


@app.route('/viewcrime', methods=['GET', 'POST'])
def viewcrime():
    postcode = request.form['postcode']
    return render_template('results.html', location=postcode)
