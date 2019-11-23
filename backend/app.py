from flask import Flask, request, jsonify, make_response
import googlemaps
from datetime import datetime
import secrets
import json
import operator
# declare constants
HOST = '0.0.0.0'
PORT = 5000

import polyline

# initialize flask application
app = Flask(__name__)

# Google maps client

gmaps = googlemaps.Client(key=secrets.API_KEY)

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
    routes = gmaps.directions(origin=start,
                              destination=end,
                              mode="walking",
                              alternatives=True,
                              departure_time=now)

    print('Possible routes: {}'.format(len(routes)))
    
    seen_lights = [None] * len(routes)
    total_lights = [0] * len(routes)
    for index, route in enumerate(routes):
        # For every route, calculate the possible lights
        ne_bound = (route['bounds']['northeast']['lat'], route['bounds']['northeast']['lng']) 
        sw_bound = (route['bounds']['southwest']['lat'], route['bounds']['southwest']['lng']) 

        """ lights = opendata.get_lights(ne_bound, sw_bound) """

        # Decode polyline for waypoints
        waypoints = polyline.decode(route['overview_polyline']['points'])

        for point in waypoints:

            """ in_range = opendata.get_in_range(point, lights, 0.050) """
            
            in_range = [{'id': '1', 'head': 1}, {'id': '2', 'head': 2}, {'id': '1', 'head': 1}]

            for rlight in in_range:
                if not seen_lights[index]:
                    seen_lights[index] = set()

                # If light has already been tracked for this path, dont track it again
                if rlight['id'] not in seen_lights[index]:
                    # If not tracked, track it and increment the total count of lights for this route
                    seen_lights[index].add(rlight['id'])
                    total_lights[index] += (1 * rlight['head'])
    
    max_light_density = 0
    max_index = -1
    max_dist = 0

    print('Lights per route: {}'.format(total_lights))
    for i in range(len(total_lights)):
        dist = routes[i]['legs'][0]['distance']['text']
        dist = dist.split(' ')            
        dist = float( dist[0] )
        total_lights[i] = total_lights[i]/dist

        # Check lights per km
        if total_lights[i] > max_light_density:
            max_light_density = total_lights[i]
            max_index = i
            max_dist = dist
        elif total_lights[i] == max_light_density:
            # If same amount of light, only change max if new one is shorter
            if dist < max_dist:
                max_light_density = total_lights[i]
                max_index = i
                max_dist = dist

    print('Weighted lights per route: {}'.format(total_lights))

    print('Best route: {}'.format(max_index+1))
    resp = make_response(jsonify(routes), 200)
    return(resp)

if __name__ == '__main__':
    app.run(host=HOST,
            debug=True,
            port=PORT)
