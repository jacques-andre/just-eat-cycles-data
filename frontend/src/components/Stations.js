// this component takes in the raw stations json from App.js and displays it "nicely".
import React from "react"
import '../index.css';

const Stations = ({ stations, isLoading }) => {
    return isLoading ? (<h1>Loading...</h1>) : (<section>
        {stations.map(station => (
            <div className="stations-wrapper">
                <div className="station-card">
                    <div className="station-name">
                        <h3>{station.station_name}</h3>
                    </div>
                    <div className="station-bikes">
                        <p><span id="bikes-aval">{station.bikes_aval}</span> / {station.docks}</p>
                    </div>
                </div>
            </div>
        ))}
    </section>)
}

export default Stations