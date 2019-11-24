#Note: Need to install geopy: pip install geopy

import string
import urllib.request, json
from geopy.distance import geodesic
import numpy as np
from numpy import linalg as LA
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString




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

            seen_lights.append({ "id":light["attributes"]["OBJECTID"], "head":val, "latitude":light["geometry"]["y"], "longitude":light["geometry"]["x"]})

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
def queryStreetTraffic(NorthEast, SouthWest, radius):

    url_send = "https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/21/query?where=1%3D1&outFields=OBJECTID,StreetName,VolumeCount,TruckRoute&geometry=" + str(SouthWest[1] - radius) + "%2C" + str(SouthWest[0] - radius) + "%2C" + str(NorthEast[1] + radius) + "%2C" + str(NorthEast[0] + radius) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json"
    print(url_send)
    with urllib.request.urlopen(url_send) as url:
        data = json.loads(url.read().decode())
        
    return data["features"]

def getRouteAvgTraffic(waypoints, roads, radius):

    total_list = []

    sum = 0
    total_distance = 0

    for i in range(len(waypoints)-1):

        point = waypoints[i]
        next_point = waypoints[i+1]

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



        on_road = []

        desired_road = 0

        max = 0

        for road in roads:

            #print("HERE")

            road_path = road["geometry"]["paths"][0]
            #print(road_path)



            for j in range(len(road_path)-1):

                A = Point(road_path[j][1],road_path[j][0])
                B = Point(road_path[j+1][1],road_path[j+1][0])

                point_path = LineString([A,B])

                
                #print(point_path)
                #light_loc = (light["geometry"]["y"], light["geometry"]["x"])

                

                if point_path.intersects(polygon):
                    if not road["attributes"]["VolumeCount"]:
                        val = 100
                    else:
                        val = road["attributes"]["VolumeCount"]
                    #print("Intersect")
                    if max == 0:
                        max = polygon.intersection(point_path).length
                        desired_road = { "id":road["attributes"]["OBJECTID"], "traffic":val, "distance":(geodesic(point, next_point).kilometers), "points":len(road_path)}
                    elif polygon.intersection(point_path).length > max:
                        desired_road = { "id":road["attributes"]["OBJECTID"], "traffic":val, "distance":(geodesic(point, next_point).kilometers)}
                        max = polygon.intersection(point_path).length

        if max != 0:
            sum += desired_road["traffic"]*desired_road["distance"]
            total_distance += desired_road["distance"]

        if max != 0:
            sum += 2000
            total_distance += geodesic(point, next_point).kilometers
        

        print(desired_road)
        #total_list.append(desired_road)

    if total_distance == 0:
        total_distance = 0.00000000001

    return sum/total_distance


# val = queryStreetTraffic((42.99568, -81.27486), (42.9936183, -81.27833), 0.01)

# #print(val)

# waypoint = [(42.99568, -81.27486), (42.99485, -81.27446), (42.994, -81.27737), (42.9939, -81.27774), (42.99387, -81.27833), (42.9936183, -81.2783156)]

# print(len(waypoint))


# #print(val[0]["geometry"]["paths"][0])
# list_new = getRouteAvgTraffic(waypoint, val, 0.0005)

# print(list_new)