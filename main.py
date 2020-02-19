import folium
import pandas
from geopy.geocoders import Nominatim
from geopy import distance
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
import ssl

data = []
same = ""
with open("locations.list", encoding="utf8", errors='ignore') as f:
    for i, line in enumerate(f):
        if i > 13:
            line = line.strip().split("\t")
            while "" in line:
                line.remove("")
            try:
                if "-" in line[1]:
                    line[1] = line[1][line[1].index("-") + 2:]
                if line[0] != same:
                    dct_line = [line[0].split(" (")[0], int(line[0].split(" (")[1][:4]), line[1]]
                    data.append(dct_line)
                same = line[0]

            except (ValueError, IndexError):
                pass

data.sort(key=lambda x: x[1])

year = int(input("Enter year: "))
center = input("Please enter your location (format: lat, long): ").split(', ')
center = tuple(center)

geolocator = Nominatim(user_agent="specify_your_app_name_here")
map = folium.Map(location=[51, 0],
                 zoom_start=4.4,
                 tiles='CartoDB dark_matter')
fg = folium.FeatureGroup(name="Film_map")
prev = ""
radius = 300
counter = 0
print("If nothing is printed for a long time - geocoder is not working, so try again later...")

for i, el in enumerate(data):

    if el[1] > year:
        break

    if year != el[1]:
        continue

    if counter == 10:
        break
        
    if el[0] != prev:
        
        location = geolocator.geocode(el[2])
        if location != None:
            lat = location.latitude
            lon = location.longitude
            dis = distance.distance(center, (lat, lon)).km
            if dis <= radius:
                print(el[0], el[1], (lat, lon))
                fg.add_child(folium.CircleMarker(location=[lat, lon], radius=8, popup=f"{year}\n movie:{el[0]}",
                                                 fill_color="#f2db24", color="#fff50d"))
                counter += 1
        
    prev = el[0]


def population():
    """
    (None) -> class 'folium.map.FeatureGroup'
    Returns population mask to add it to the map
    """
    population_mask = folium.FeatureGroup(name="Population")
    population_mask.add_child(
        folium.GeoJson(data=open('../lab2.2/world.json', 'r',
                                 encoding='utf-8-sig').read(),
                       style_function=lambda x: {'fillColor': '#EE2376'  # pink
                       if x['properties']['POP2005'] < 100000
                       else '#81DC1A' if 100000 <= x['properties'][
                           'POP2005'] < 200000  # green
                       else '#B6E80E' if 200000 <= x['properties'][
                           'POP2005'] < 1000000  # light green
                       else '#5503E5' if 1000000 <= x['properties'][
                           'POP2005'] < 2000000  # purple
                       else '#E57703' if 2000000 <= x['properties'][
                           'POP2005'] < 9000000  # orange
                       else '#0EE896' if 9000000 <= x['properties'][
                           'POP2005'] < 15000000  # blue
                       else '#E112B5' if 15000000 <= x['properties'][
                           'POP2005'] < 20000000  # pink
                       else '#3882EC'}))  # dark blue
    return population_mask


print("You are lucky to catch geocoder working, check your map and have a nice day")


population_mask = population()
map.add_child(population_mask)
map.add_child(fg)
map.save('Map_6.html')

