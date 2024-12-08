import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

function WorldMap({ location, setLocation }) {
  const mapRef = useRef(null);
  const markerRef = useRef(null);

  useEffect(() => {
    // Initialize the map
    const map = L.map("map").setView([20.5937, 78.9629], 5); // Default to India
    mapRef.current = map;

    // Add tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    // Custom pin marker
    const pinIcon = L.icon({
      iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
    });

    // Handle map clicks
    map.on("click", async (e) => {
      const { lat, lng } = e.latlng;

      // Reverse geocode the clicked location
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
      );
      const data = await response.json();
      const placeName = data?.display_name || "Unknown location";

      // Update location state
      setLocation({ name: placeName, lat, lng });

      // Update the marker
      if (markerRef.current) {
        map.removeLayer(markerRef.current);
      }
      markerRef.current = L.marker([lat, lng], { icon: pinIcon }).addTo(map);
    });

    return () => {
      map.remove(); // Clean up the map on unmount
    };
  }, [setLocation]);

  useEffect(() => {
    if (location?.lat && location?.lng) {
      const map = mapRef.current;

      // Fly to the new location
      map.flyTo([location.lat, location.lng], 10);

      // Update the marker
      if (markerRef.current) {
        map.removeLayer(markerRef.current);
      }

      const pinIcon = L.icon({
        iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
      });

      markerRef.current = L.marker([location.lat, location.lng], { icon: pinIcon }).addTo(map);
    }
  }, [location]);

  return <div id="map" style={{ height: "500px", width: "100%" }}></div>;
}

export default WorldMap;