
"""
This is to run on Python 2.7 on a RaspberryPI
With an attached Adafruit Ultimate GPS connected via USB
"""
import datetime
from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)


class Location:
    """
    Physical location with latitude, longitude, altitude (feet above sea level)
    """

    def __init__(self, lat, lon, alt):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        self.created_dt = str(datetime.datetime.now())

    def __repr__(self):
        return "<Location {0}, {1} @ {2} Feet Above Sea Level ".format(self.latitude, self.longitude, self.altitude)

    def as_dict(self):
        return {'lat': self.latitude, 'lon': self.longitude, 'alt': self.altitude, 'dtg': self.created_dt}


current_location = Location(32.0000000, -97.0000000, 550)


@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None


@app.route('/')
def hello_world():
    return "Navigate to /api/v0.1/location for current location"


@app.route('/api/v0.1/location', methods=["GET"])
@auth.login_required
def get_location():
    return jsonify(current_location.as_dict())


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run()
