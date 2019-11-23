from flask import Flask, request, jsonify, make_response
import googlemaps
from datetime import datetime

# declare constants
HOST = '0.0.0.0'
PORT = 5000

import polyline

# initialize flask application
app = Flask(__name__)

# Google maps client

gmaps = googlemaps.Client(key='test')

# Debug variable
DEBUG = True

# Safest path
# Usage: IP:HOST/api/path?from=LAT,LON&to=LAT,LON
# Example: http://0.0.0.0:5000/api/path?from=43.004663,-81.276361&to=42.993940,-81.276805
@app.route('/api/path', methods=['GET'])
def safe_path():
    # Response header
    headers = {"Content-Type": "application/json"}

    # Grab data from requests
    start = request.args.get('from')
    end = request.args.get('to')
    
    if DEBUG:
        print('Start coordinates: {}'.format(start))
        print('End coordinates: {}'.format(end))

    # Query Directions API from start to end
    now = datetime.now()
    result = gmaps.directions(origin=start,
                              destination=end,
                              mode="walking",
                              alternatives=True,
                              departure_time=now)
                              
    return(jsonify(directions_result))

    #Get google maps path


    # Iterate and calculate distances based on location on street lights


    # return safest path

    return "Hello"

if __name__ == '__main__':
    r = polyline.decode("ihleGtkaoNoCiNgDnAkAh@QBSCiAm@Qj@u@pA[\\i@b@IFKSWe@c@g@KUQs@yAr@[DwKeBKEa@e@k@y@KEo@KsCa@iAOc@CM@[JEQScAI_@a@f@uAFAEG[SKFnDBh@C@{CLUGGtB_@?B|@B\\N^FR`@r@?d@[?E@CD?H")
    app.run(host=HOST,
            debug=True,
            port=PORT)
