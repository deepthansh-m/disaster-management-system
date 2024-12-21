import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";
import WorldMap from "../components/WorldMap";
import apiService from "../services/api_service";

function HomePage() {
  const [location, setLocation] = useState({ name: "", lat: null, lng: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  // Fetch prediction based on the location
  const fetchPrediction = async (locationData) => {
    try {
      setLoading(true);
      const data = await apiService.getPrediction(locationData);

      if (data && data.result) {
        // Return the prediction data to the SearchBar for navigation
        return data;
      }
    } catch (err) {
      console.error("Error fetching prediction:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="homepage">
      <h1>Disaster Management System</h1>
      <SearchBar
        location={location}
        setLocation={setLocation}
        fetchPrediction={fetchPrediction}
      />
      <WorldMap location={location} setLocation={setLocation} />
    </div>
  );
}

export default HomePage;
