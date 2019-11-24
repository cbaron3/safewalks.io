#Note: Need to install geopy: pip install geopy

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
                val = int(light["attributes"]["PublicCartoSymbolType"].split('-')[1].split('H')[0])

            seen_lights.append({ "id":light["attributes"]["OBJECTID"], "head":val })

    return seen_lights
    

#Get points vector





#print(x)


#print("https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=PublicCartoSymbolType,RoadClass&geometry=" + str(-81.223) + "%2C" + str(42.960) + "%2C" + str(-81.213) + "%2C" + str(42.962) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json")

#val = queryAreaLights((43.963, -80.218), (41.961, -82.220), 0.005)

#print(val[0]["geometry"]["x"])

#print(len(val))

#seen_light = getSeenLights((42.96182434078348, -81.21924500849471), (42.961085612640474,-81.21750025760407), val, 1)

#print(seen_light)




#Use a similar method to return the traffic volumes for the route taken and the sidewalk availability for the route taken

#Returns a list of street points in the given area
# def queryAreaLights(NorthEast, SouthWest):

#     url_send = "https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=PublicCartoSymbolType,OBJECTID&geometry=" + str(SouthWest[1]) + "%2C" + str(SouthWest[0]) + "%2C" + str(NorthEast[1]) + "%2C" + str(NorthEast[0]) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json"

#     with urllib.request.urlopen(url_send) as url:
#         data = json.loads(url.read().decode())
        
#     return data["features"]