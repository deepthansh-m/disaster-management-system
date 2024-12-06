const BASE_URL = 'http://localhost:5000/api';

// Error handling wrapper
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'API request failed');
    }
    return response.json();
};

// API endpoints
const apiService = {
    // Disaster endpoints
    getDisasters: async () => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'GET',
            credentials: 'include', // Add credentials for CORS
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return handleResponse(response);
    },

    addDisaster: async (disasterData) => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'POST',
            credentials: 'include', // Add credentials for CORS
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(disasterData)
        });
        return handleResponse(response);
    },

    // Prediction endpoints
    getPrediction: async (location) => {
        const response = await fetch(`${BASE_URL}/predictions?location=${encodeURIComponent(location)}`, {
            method: 'GET',
            credentials: 'include', // Add credentials for CORS
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return handleResponse(response);
    },

    submitPrediction: async (predictionData) => {
        const response = await fetch(`${BASE_URL}/predictions/predict/`, {
            method: 'POST',
            credentials: 'include', // Add credentials for CORS
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(predictionData)
        });
        return handleResponse(response);
    },

    // Weather endpoints
    getWeatherData: async (location) => {
        const response = await fetch(`${BASE_URL}/weather?location=${encodeURIComponent(location)}`, {
            method: 'GET',
            credentials: 'include', // Add credentials for CORS
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return handleResponse(response);
    }
};

export default apiService;
