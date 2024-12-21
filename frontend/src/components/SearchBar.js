import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate

function SearchBar({ location, setLocation, fetchPrediction }) {
  const [query, setQuery] = useState("");
  const navigate = useNavigate(); // Initialize useNavigate

  const handleSearch = async () => {
    if (!query.trim()) return;

    // Geocode query using OpenStreetMap API
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${query}`
    );
    const data = await response.json();

    if (data.length > 0) {
      const { lat, lon, display_name } = data[0];
      const newLocation = {
        name: display_name,
        lat: parseFloat(lat),
        lng: parseFloat(lon),
      };
      setLocation(newLocation);

      // Call the prediction API with the formatted location
      try {
        const prediction = await fetchPrediction({
          latitude: newLocation.lat,
          longitude: newLocation.lng,
          location: display_name,
        });

        // Navigate to the details page and pass the prediction data via state
        navigate(`/details`, { state: { prediction } });
      } catch (error) {
        console.error("Error fetching prediction:", error);
        alert("Failed to fetch prediction data.");
      }
    } else {
      alert("Location not found");
    }
  };

  // Update query field when location changes (bidirectional sync)
  useEffect(() => {
    if (location?.name) {
      setQuery(location.name);
    }
  }, [location]);

  // Trigger search when the user presses Enter
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search for location..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown} // Search when Enter is pressed
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchBar;
