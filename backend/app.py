from flask import Flask, request, jsonify, make_response
import googlemaps
from datetime import datetime
import secrets
import json
import operator
import opendata
import urllib.request
import requests

# Handling cross origin resource handling


# declare constants
HOST = '0.0.0.0'
PORT = 5000

import polyline

# initialize flask application
app = Flask(__name__)

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Google maps client

gmaps = googlemaps.Client(key=secrets.API_KEY)

# Debug variable
DEBUG = True

# Safest path
# Usage: IP:HOST/api/path?from=LAT,LON&to=LAT,LON
# Example: http://0.0.0.0:5000/api/path?from=43.004663,-81.276361&to=248 Trott Dr
@app.route('/api/path', methods=['GET'])
def safe_path():
    print(request.args)
    # Grab data from requests
    start = request.args.get('from')
    end = request.args.get('to')
    end = gmaps.geocode(end)
    end = (end[0]['geometry']['location']['lat'], end[0]['geometry']['location']['lng'])
    
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
    tracked_lights = [None] * len(routes)

    total_lights = [0] * len(routes)
    for index, route in enumerate(routes):
        # For every route, calculate the possible lights
        ne_bound = (route['bounds']['northeast']['lat'], route['bounds']['northeast']['lng']) 
        sw_bound = (route['bounds']['southwest']['lat'], route['bounds']['southwest']['lng']) 
        available_lights = opendata.queryAreaLights(ne_bound, sw_bound, 0.00025)

        # Decode polyline for waypoints
        waypoints = polyline.decode(route['overview_polyline']['points'])
        # Add start and stop points to waypoints
        start = start.split(',')
        waypoints.insert(0, (float(start[0]),float(start[1]) ) )
        waypoints.append((float(end[0]),float(end[1]) ) )
        print(waypoints)
        print('{} waypoints for route {}'.format(len(waypoints), index+1))
        for i in range(len(waypoints) - 1):
            point = waypoints[i]
            next_point = waypoints[i+1]
            
            in_range = opendata.getSeenLights(point, next_point, available_lights, 0.0005)
            for rlight in in_range:
                if not seen_lights[index]:
                    seen_lights[index] = set()
                
                if not tracked_lights[index]:
                    tracked_lights[index] = list()

                # If light has already been tracked for this path, dont track it again
                if rlight['id'] not in seen_lights[index]:
                    # If not tracked, track it and increment the total count of lights for this route
                    seen_lights[index].add(rlight['id'])
                    tracked_lights[index].append(rlight)
                    total_lights[index] += (1 * rlight['head'])
    
    max_light_density = 0
    max_index = -1
    max_dist = 0

    print('Lights for each route: {}'.format(total_lights))
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

    print('Weighted lights for each route: {}'.format(total_lights))
    print('Best route: {}'.format(max_index+1))
    
    # Return as a response a list of routes with their corresponding tracked lights and their bounding box lights and their safety rating
    safety_result = []
    for i in range(len(routes)):
        safety_result.append( {
            'rating': total_lights[i],
            'polyline': routes[i]['overview_polyline']['points'],
            'area_lights' : list(seen_lights[i]),
            'in_range_lights': tracked_lights[i]
        } )

    safety_result = json.dumps(safety_result)
    resp = make_response(safety_result, 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return(resp)

if __name__ == '__main__':
    app.run(host=HOST,
            debug=True,
            port=PORT)