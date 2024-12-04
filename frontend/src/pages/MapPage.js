import React from "react";
import DisasterPredictionChart from "../components/DisasterPredictionChart";

function MapPage() {
    return (
        <div className="map-page">
            <h2>Map and Prediction Data</h2>
            <DisasterPredictionChart />
        </div>
    );
}

export default MapPage;
