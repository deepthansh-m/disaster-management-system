import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import WorldMap from "../components/WorldMap";

function HomePage() {
  const [location, setLocation] = useState({
    name: "",
    lat: null,
    lng: null,
  });

  return (
    <div className="homepage">
      <h1>Disaster Management System</h1>
      <SearchBar location={location} setLocation={setLocation} />
      <WorldMap location={location} setLocation={setLocation} />
    </div>
  );
}

export default HomePage;