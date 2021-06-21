// This is the main entry point of the frontend. All data is fetched from here and then outsourced to other components.
import React, { useEffect,useState } from 'react';
import axios from "axios";
import './index.css';
import Stations from "./components/Stations"

function App() {
  const [stations,setStations] = useState([]);
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchStations = async () => {
      const result = await axios(`/stations`);

      setStations(result.data)
      setIsLoading(false)
    }
    fetchStations()
  },[])

  return(
    <div className="container">
      <Stations isLoading={isLoading} stations={stations}/>
    </div>
  );
}

export default App;
