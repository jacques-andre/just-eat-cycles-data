// this component takes in the raw stations json from App.js and displays it "nicely".
import React from "react"
import '../index.css';

const Stations = ({ stations, isLoading }) => {
    return isLoading ? (<h1>Loading...</h1>) : (<div className="stations-wrapper">
        {stations.map(station => (
                <div className="station-card">
                    <div className="station-name">
                        <h3>{station.station_name}</h3>
                    </div>
                    <div className="station-bikes">
                        <p><span id="bikes-aval">{station.bikes_aval}</span> / {station.docks}</p>
                        <p>bikes avaliable</p>
                    </div>
                </div>
        ))}
    </div>)
}

export default Stations