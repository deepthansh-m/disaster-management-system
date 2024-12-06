// frontend/src/pages/HomePage.js
import React, { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import WorldMap from "../components/WorldMap";
import apiService from '../services/api_service';

function HomePage() {
    const [disasters, setDisasters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchDisasters = async () => {
        try {
            setLoading(true);
            const data = await apiService.getDisasters();
            setDisasters(data);
        } catch (error) {
            console.error('Failed to fetch disasters:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDisasters();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="homepage">
            <h1>Disaster Prediction System</h1>
            <SearchBar />
            <WorldMap disasters={disasters} />
        </div>
    );
}

export default HomePage;