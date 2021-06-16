import requests
import pprint
import json
from flask import Flask, jsonify

r = requests.get(
    "https://gbfs.urbansharing.com/edinburghcyclehire.com/station_status.json"
)
station_status_json = r.json()

r = requests.get(
    "https://gbfs.urbansharing.com/edinburghcyclehire.com/station_information.json"
)
station_information_json = r.json()

station_data = station_status_json["data"]["stations"]  # avaliable bikes,docks
station_info = station_information_json["data"][
    "stations"
]  # station name,lat/lon,address


stations = list()  # holds Station objects for each station


app = Flask(__name__)


class Station(object):
    bikes_aval = 0
    docks = 0
    station_name = ""
    station_id = 0

    def __init__(self, bikes_aval, docks, station_name, station_id):
        self.bikes_aval = bikes_aval
        self.docks = docks
        self.station_name = station_name
        self.station_id = station_id

    def __str__(self):
        return f"id: {self.station_id}, name: {self.station_name}, bikes_aval: {self.bikes_aval}/{self.docks}"

    def toJSON(self):
        return {
            "station_id": self.station_id,
            "station_name": self.station_name,
            "bikes_aval": self.bikes_aval,
            "docks": self.docks,
        }


def get_station_name(station_id: int) -> str:
    # returns station name from station id
    for station in station_info:
        # station vars
        current_station_id = station["station_id"]

        if current_station_id == str(station_id):
            return station["name"]
    return None  # no station found


def gen_stations():
    # aggregates all stations from api into objects
    for station in station_data:
        # station vars
        station_id = int(station["station_id"])
        station_name = get_station_name(station_id)
        bikes_aval = station["num_bikes_available"]
        docks = station["num_docks_available"]

        s = make_station_object(bikes_aval, docks, station_name, station_id)
        stations.append(s)


def make_station_object(bikes_aval, docks, station_name, station_id):
    # creates a Station object
    station = Station(bikes_aval, docks, station_name, station_id)
    return station


@app.route("/")
def all_stations():
    # returns all stations in json format
    json_stations = list()
    for s in stations:
        json_stations.append(s.toJSON())
    json_stations.sort(
        key=lambda x: x["bikes_aval"], reverse=True
    )  # sorts in terms of bikes avaliable
    return json.dumps(json_stations)


@app.route("/biggest_station_bikes")
def find_biggest_station():
    # returns the biggest station based on how many number of bikes avaliable.
    biggest = 0
    max_station = None
    for station in stations:
        if station.bikes_aval >= biggest:
            biggest = station.bikes_aval
            max_station = station
    return max_station.toJSON()


@app.route("/biggest_station_docks")
def find_biggest_station_docks():
    # returns the biggest station based on how many number of docks avaliable.
    biggest = 0
    max_station = None
    for station in stations:
        if station.docks >= biggest:
            biggest = station.docks
            max_station = station
    return max_station.toJSON()


gen_stations()
app.run()
