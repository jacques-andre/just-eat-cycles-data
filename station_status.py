import requests
import pprint
import json

r = requests.get("https://gbfs.urbansharing.com/edinburghcyclehire.com/station_status.json")
station_status_json = r.json()

r = requests.get("https://gbfs.urbansharing.com/edinburghcyclehire.com/station_information.json")
station_information_json = r.json()

station_data = station_status_json['data']['stations'] # avaliable bikes,docks
station_info = station_information_json['data']['stations'] # station name,lat/lon,address


stations = set() # holds individual stations

class Station(object):
    bikes_aval = 0
    docks = 0
    station_name = ""
    station_id = 0

    def __init__(self,bikes_aval,docks,station_name,station_id):
        self.bikes_aval = bikes_aval
        self.docks = docks
        self.station_name = station_name
        self.station_id = station_id

    def __str__(self):
        return f"id: {self.station_id}, name: {self.station_name}, bikes_aval: {self.bikes_aval}/{self.docks}"


def get_station_name(station_id: int) -> str:
    # returns station name from station id

    for station in station_info:
        # station vars
        current_station_id = station["station_id"]

        if current_station_id == str(station_id):
            return station["name"]
    return "" # no station found

def get_station_status():
    # aggregates all stations from api into objects
    for station in station_data:
        # station vars
        station_id = int(station["station_id"])
        station_name = get_station_name(station_id)
        bikes_aval = station["num_bikes_available"]
        docks = station["num_docks_available"]

        s = make_station(bikes_aval,docks,station_name,station_id)
        stations.add(s)

def make_station(bikes_aval,docks,station_name,station_id):
    station = Station(bikes_aval,docks,station_name,station_id)
    return station

def find_biggest_station() -> int:
    biggest = 0
    max_station = None
    for station in stations:
        if station.bikes_aval >= biggest:
            biggest = station.bikes_aval
            max_station = station
    return max_station

def print_all_stations():
    for s in stations:
        print(s)

def main():
    get_station_status()
    biggest_station = find_biggest_station()
    print(f"The biggest station is: {biggest_station.station_name}, bikes_aval: {biggest_station.bikes_aval}/{biggest_station.docks}")
    # print_all_stations()

main()
