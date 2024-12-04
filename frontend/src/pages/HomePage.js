import React from "react";
import SearchBar from "../components/SearchBar";
import WorldMap from "../components/WorldMap";

function HomePage() {
    return (
        <div className="homepage">
            <h1>Disaster Prediction System</h1>
            <SearchBar />
            <WorldMap />
        </div>
    );
}

export default HomePage;
