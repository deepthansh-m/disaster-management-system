const API_BASE_URL = "http://localhost:5000/api";

export const fetchWeatherData = async (location) => {
    try {
        const response = await fetch(`${API_BASE_URL}/weather/current?location=${location}`);
        return response.json();
    } catch (error) {
        console.error("Error fetching weather data:", error);
        return null;
    }
};

export const fetchPredictionData = async (data) => {
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        return response.json();
    } catch (error) {
        console.error("Error fetching prediction data:", error);
        return null;
    }
};
