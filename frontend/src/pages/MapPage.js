import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useHistory } from "react-router-dom"; // For navigation
import DisasterPredictionChart from "../components/DisasterPredictionChart";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS
import L from "leaflet"; // Import Leaflet

function MapPage() {
  const [coordinates, setCoordinates] = useState({ lat: 51.505, lng: -0.09 }); // Default coordinates (can be adjusted)
  const history = useHistory();

  const handleMapClick = (e) => {
    const { lat, lng } = e.latlng;
    setCoordinates({ lat, lng });

    // Navigate to a details page on marker click
    history.push({
      pathname: "/disaster-details",
      state: { lat, lng },
    });
  };

  return (
    <div className="map-page">
      <h2>Map and Prediction Data</h2>

      {/* Leaflet map setup */}
      <MapContainer
        center={[coordinates.lat, coordinates.lng]}
        zoom={13}
        style={{ height: "500px", width: "100%" }}
        onClick={handleMapClick} // Handling click event to set coordinates
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <Marker position={[coordinates.lat, coordinates.lng]}>
          <Popup>
            <div>
              <h4>Disaster Prediction Details</h4>
              {/* Display disaster prediction info here */}
              <DisasterPredictionChart />
            </div>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default MapPage;
