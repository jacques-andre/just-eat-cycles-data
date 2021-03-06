import time
import json
from termcolor import cprint
from flask import Flask, jsonify

station_status_json = open("json_data/station_status.json")
station_information_json = open("json_data/station_information.json")
station_data = json.load(station_status_json)["data"][
    "stations"
]  # avaliable bikes,docks
station_info = json.load(station_information_json)["data"][
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


def refresh_json_data():
    # "refreshes" the latest data from local json file
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    cprint(f"refreshed json data.. ({current_time})", "yellow")

    global station_status_json
    global station_information_json
    global station_data
    global station_info

    # open json files and parse
    station_status_json = open("json_data/station_status.json")
    station_information_json = open("json_data/station_information.json")

    station_data = json.load(station_status_json)["data"][
        "stations"
    ]  # avaliable bikes,docks
    station_info = json.load(station_information_json)["data"][
        "stations"
    ]  # station name,lat/lon,address

    stations.clear()  # clear initial stations before "refreshing"
    gen_stations()


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


# routes
@app.route("/stations")
def all_stations():
    # returns all stations in json format
    refresh_json_data()
    json_stations = list()
    for s in stations:
        json_stations.append(s.toJSON())
    json_stations.sort(
        key=lambda x: x["bikes_aval"], reverse=True
    )  # sorts in terms of bikes avaliable
    return json.dumps(json_stations, indent=4, separators=(",", ": "))


@app.route("/biggest_station_bikes")
def biggest_station_bikes():
    refresh_json_data()
    # returns the biggest station based on how many number of bikes avaliable.
    biggest = 0
    max_station = None
    for station in stations:
        if station.bikes_aval >= biggest:
            biggest = station.bikes_aval
            max_station = station
    return max_station.toJSON()


@app.route("/stations_aval")
def stations_aval():
    refresh_json_data()
    # return all stations aval
    station_count = {"bikes": 0, "docks": 0, "percent": 0}

    for station in stations:
        station_count["bikes"] += int(station.bikes_aval)
        station_count["docks"] += int(station.docks)

    station_count["percent"] = round((station_count["bikes"] / station_count["docks"]) * 100,2)

    return jsonify(station_count)


@app.route("/biggest_station_docks")
def biggest_station_docks():
    refresh_json_data()
    # returns the biggest station based on how many number of docks avaliable.
    biggest = 0
    max_station = None
    for station in stations:
        if station.docks >= biggest:
            biggest = station.docks
            max_station = station
    return max_station.toJSON()


@app.route("/station/<station_identifier>")
def get_station(station_identifier):
    refresh_json_data()
    # returns a station by station id or station name

    # check if id (int) or name (str) passed
    try:
        # station_identifier is an id
        station_id = int(station_identifier)
        for station in stations:
            if station.station_id == station_id:
                return station.toJSON(), 200
    except:
        # station_identifier is a name
        for station in stations:
            if station_identifier.lower() in station.station_name.lower():
                return station.toJSON(), 200
    return "station not found!", 404


app.run()
