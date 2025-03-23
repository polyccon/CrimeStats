import os

from flask import jsonify, request, abort, make_response, render_template, redirect, send_file, url_for, \
    send_from_directory

from src.core import app
from src.data.convert_data import CrimeDataProcessor


def _parse_request_body():
    """Extract data type from request body."""
    request_body = request.get_json()
    try:
        id_ = request_body["id"]
        items = request_body["items"]
        return id_, items
    except KeyError:
        # Missing necessary fields.
        response_body = {"error": "'id', 'items' key in request body"}
        abort(make_response(jsonify(response_body), 400))


@app.route("/healthz", methods=["GET"])
def healthz():
    return "", 200


# @app.route("/")
# def hello():
#     return render_template("home.html")


# @app.route("/home")
# def home():
#     return redirect("/")

@app.route("/")
def home():
    """Redirect to the heatmap page with London's central coordinates."""
    default_lat = 51.5074  # Central London (Charing Cross)
    default_lng = -0.1278
    return redirect(url_for("get_heatmap", lat=default_lat, lng=default_lng))


@app.route("/category_data/<location>")
def category_data(location):
    processor = CrimeDataProcessor(location)
    return jsonify(processor.get_crime_categories())


@app.route("/outcome_data/<location>")
def outcome_data(location):
    processor = CrimeDataProcessor(location)
    return jsonify(processor.get_crime_outcomes())


@app.route("/viewcrime", methods=["GET", "POST"])
def viewcrime():
    postcode = request.form["postcode"]
    return render_template("results.html", location=postcode)


@app.route("/heatmap_data")
def heatmap_data():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    # Fetch crime data based on lat and lng (this could be from an API or database)
    processor = CrimeDataProcessor(lat, lng)
    crime_data = processor.fetch_crime_data()

    return jsonify({"crimes": crime_data})


@app.route("/heatmap", methods=["GET"])
def get_heatmap():
    """API endpoint to fetch and return heatmap HTML content."""
    try:
        lat = request.args.get("lat", default="51.5074")
        lng = request.args.get("lng", default="-0.1278")

        if lat is None or lng is None:
            return jsonify({"error": "Missing required parameters: lat, lng"}), 400

        lat, lng = float(lat), float(lng)

        # Generate heatmap based on location
        processor = CrimeDataProcessor(lat, lng)
        map_filename = processor.generate_heatmap()

        # Read only the heatmap HTML content
        with open(map_filename, "r", encoding="utf-8") as file:
            map_html_content = file.read()

        # If this is an AJAX request (dynamic update), return only the map HTML
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return map_html_content  # Only return the updated heatmap

        # Otherwise, render the full heatmap.html (for first page load)
        return render_template("heatmap.html", lat=lat, lng=lng, map_html_content=map_html_content)

    except ValueError as e:
        return jsonify({"error": f"Invalid parameter value: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


