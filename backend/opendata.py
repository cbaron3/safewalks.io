import string
import urllib.request, json
from geopy.distance import geodesic
import numpy as np
from numpy import linalg as LA
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#Returns a list of street lights in the given area
def queryAreaLights(NorthEast, SouthWest, radius):

    url_send = "https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=PublicCartoSymbolType,OBJECTID&geometry=" + str(SouthWest[1] - radius) + "%2C" + str(SouthWest[0] - radius) + "%2C" + str(NorthEast[1] + radius) + "%2C" + str(NorthEast[0] + radius) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json"

    with urllib.request.urlopen(url_send) as url:
        data = json.loads(url.read().decode())
        
    return data["features"]

#Gets seen lights at given point as a list of dictionaries, within certain radius in KM
def getSeenLights(point, next_point, lights, radius):

    #Calculate bounding box for waypoints: Frist get edge vector at 0,0, but perpendicular (get perpendicular vector {X, Y} becomes {x, -y})
    edge = np.array([[0,0],[next_point[0] - point[0], point[1] - next_point[1]]])

    #Get unit vector and multiply by desired radius (arbitrary units) and opposite vector
    edge_perp_radius = np.true_divide(edge, LA.norm(edge))*radius
    neg_edge_perp_radius = -edge_perp_radius

    #Get four points for polygon using vector for edge on passed points
    point_1 = [point[0] + edge_perp_radius[1][1], point[1] + edge_perp_radius[1][0]]
    point_2 = [point[0] + neg_edge_perp_radius[1][1], point[1] + neg_edge_perp_radius[1][0]]
    point_3 = [next_point[0] + edge_perp_radius[1][1], next_point[1] + edge_perp_radius[1][0]]
    point_4 = [next_point[0] + neg_edge_perp_radius[1][1], next_point[1] + neg_edge_perp_radius[1][0]]

    lat_lon_area = np.array([point_1, point_2, point_4, point_3])

    #Generate polygon representing area to check for lights
    polygon = Polygon(lat_lon_area)


    seen_lights = []

    for light in lights:
        light_loc = Point(light["geometry"]["y"], light["geometry"]["x"])
        #light_loc = (light["geometry"]["y"], light["geometry"]["x"])
        if polygon.contains(light_loc):
            if not light["attributes"]["PublicCartoSymbolType"]:
                val = 1
            else:
                try:
                    val = int(light["attributes"]["PublicCartoSymbolType"].split('-')[1].split('H')[0])
                except:
                    val = 1

            seen_lights.append({ "id":light["attributes"]["OBJECTID"], "head":val, "latitude":light["geometry"]["y"], "longitude":light["geometry"]["x"]})

    return seen_lights