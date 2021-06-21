import React from 'react';
import './App.css';

function App() {
  const [biggestStationName, setBiggestStationName] = React.useState();

  fetch('/biggest_station_bikes')
    .then(res => res.json())
    .then((data) => {
      setBiggestStationName(data['station_name'])
    })
    .catch(console.log)

  fetch('/stations')
    .then(res => res.json())
    .then((data) => {
      console.log(data)
      for (let index = 0; index < data.length; index++) {
        console.log(data[index]);
      }
    })
    .catch(console.log)
  return (
    <div className="App">
      <h1>Current Biggest Station: {biggestStationName}</h1>
    </div>
  );
}

export default App;
