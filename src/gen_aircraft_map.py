# Simple tool for generating a local map out of the aircraft data saved into the sqlite DB using folium
# Bjoern Heller <tec(att)sixtopia.net>

import sqlite3
import folium

DATABASE_FILE = "aircraft_data.db"

def get_aircraft_positions():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''SELECT latitude, longitude, flight FROM aircraft_data''')
    aircraft_positions = c.fetchall()
    conn.close()
    return aircraft_positions

def generate_web_map(aircraft_positions):
    valid_positions = [(float(lat), float(lon), flight) for lat, lon, flight in aircraft_positions if lat != 'N/A' and lon != 'N/A']

    if not valid_positions:
        print("No valid positions found.")
        return

    lat_sum, lon_sum = 0.0, 0.0

    for lat, lon, _ in valid_positions:
        lat_sum += lat
        lon_sum += lon

    map_center = (lat_sum / len(valid_positions), lon_sum / len(valid_positions))
    my_map = folium.Map(location=map_center, zoom_start=5)

    for lat, lon, flight in valid_positions:
        popup_text = f"Flight: {flight}<br>Latitude: {lat}<br>Longitude: {lon}"
        folium.Marker(location=(lat, lon), popup=popup_text).add_to(my_map)

    my_map.save("aircraft_map.html")

if __name__ == "__main__":
    aircraft_positions = get_aircraft_positions()
    generate_web_map(aircraft_positions)

