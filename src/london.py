#Note: Need to install geopy: pip install geopy

import string
import urllib.request, json
from geopy.distance import geodesic



#Returns a list of street lights in the given area
def queryAreaLights(NorthEast, SouthWest):

    url_send = "https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=PublicCartoSymbolType,OBJECTID&geometry=" + str(SouthWest[1]) + "%2C" + str(SouthWest[0]) + "%2C" + str(NorthEast[1]) + "%2C" + str(NorthEast[0]) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json"

    with urllib.request.urlopen(url_send) as url:
        data = json.loads(url.read().decode())
        
    return data["features"]

#Gets seen lights at given point as a list of dictionaries, within certain radius in KM
def getSeenLights(point, lights, radius):

    seen_lights = []

    for light in lights:
        light_loc = (light["geometry"]["y"], light["geometry"]["x"])
        if geodesic(point, light_loc).kilometers <= radius:
            val = int(light["attributes"]["PublicCartoSymbolType"].split('-')[1].split('H')[0])
            seen_lights.append({ "id":light["attributes"]["OBJECTID"], "head":val })

    return seen_lights




#print("https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=PublicCartoSymbolType,RoadClass&geometry=" + str(-81.223) + "%2C" + str(42.960) + "%2C" + str(-81.213) + "%2C" + str(42.962) + "&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json")

#val = queryAreaLights((42.963, -81.218), (42.961, -81.220))

#print(val[0]["geometry"]["x"])

#print(len(val))

#seen_light = getSeenLights((42.96165984399018, -81.21898237620404), val, 0.03)

#print(seen_light)