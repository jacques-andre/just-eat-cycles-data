// This is the main entry point of the frontend. All data is fetched from here and then outsourced to other components.
import React, { useEffect,useState } from 'react';
import axios from "axios";
import './index.css';
import Stations from "./components/Stations"

function App() {
  const [stations,setStations] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [allBikes,setAllBikes] = useState()

  useEffect(() => {
    const fetchStations = async () => {
      const result = await axios(`/stations`);

      setStations(result.data)
      setIsLoading(false)
    }
    const fetchAllBikes = async () => {
      const result = await axios(`/stations_aval`)
      setAllBikes(result.data)
      setIsLoading(false)
    }
    fetchStations()
    fetchAllBikes()
  },[])

  return(
    <div className="container">
      <h2>Station Map</h2>
      <Stations isLoading={isLoading} stations={stations} allBikes={allBikes}/>
    </div>
  );
}

export default App;
