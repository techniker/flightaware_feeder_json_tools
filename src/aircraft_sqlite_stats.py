import requests
import time
import sqlite3

DATABASE_FILE = "aircraft_data.db"
MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS aircraft_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 flight TEXT,
                 hex_code TEXT,
                 squawk TEXT,
                 altitude_baro TEXT,
                 altitude_geom TEXT,
                 heading TEXT,
                 ground_speed TEXT,
                 vertical_speed TEXT,
                 latitude TEXT,
                 longitude TEXT,
                 origin_country TEXT,
                 icao24 TEXT,
                 last_contact TEXT,
                 on_ground TEXT,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO aircraft_data
                 (flight, hex_code, squawk, altitude_baro, altitude_geom, heading,
                 ground_speed, vertical_speed, latitude, longitude, origin_country,
                 icao24, last_contact, on_ground)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

def get_aircraft_data():
    url = "http://flightawarefeeder01.turm.ak.ber.sixtopia.net/skyaware/data/aircraft.json?"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.ConnectionError, requests.HTTPError) as e:
            print(f"Failed to get aircraft data: {e}")
            retries += 1
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    print(f"Max retries reached, unable to retrieve aircraft data.")
    return None

def display_aircraft_data(aircraft_list):
    for aircraft in aircraft_list:
        flight_data = aircraft.get('flight', 'N/A')
        hex_code = aircraft.get('hex', 'N/A')
        squawk = aircraft.get('squawk', 'N/A')
        altitude_baro = aircraft.get('alt_baro', 'N/A')
        altitude_geom = aircraft.get('alt_geom', 'N/A')
        heading = aircraft.get('heading', 'N/A')
        ground_speed = aircraft.get('gs', 'N/A')
        vertical_speed = aircraft.get('vs', 'N/A')
        latitude = aircraft.get('lat', 'N/A')
        longitude = aircraft.get('lon', 'N/A')
        origin_country = aircraft.get('country', 'N/A')
        icao24 = aircraft.get('icao24', 'N/A')
        last_contact = aircraft.get('last_contact', 'N/A')
        on_ground = aircraft.get('on_ground', 'N/A')

        aircraft_data = (flight_data, hex_code, squawk, altitude_baro, altitude_geom, heading,
                         ground_speed, vertical_speed, latitude, longitude, origin_country,
                         icao24, last_contact, on_ground)

        insert_data(aircraft_data)

        print("Aircraft Data:")
        for key, value in aircraft.items():
            print(f"{key}: {value}")
        print("----")
        print("\n")

def get_aircraft_count():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM aircraft_data")
    count = c.fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    create_table()
    while True:
        aircraft_data = get_aircraft_data()
        if aircraft_data:
            display_aircraft_data(aircraft_data["aircraft"])
        aircraft_count = get_aircraft_count()
        print(f"Number of aircraft fixes in database: {aircraft_count}")
        time.sleep(0.1)

