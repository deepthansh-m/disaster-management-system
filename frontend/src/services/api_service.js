// api_service.js
const BASE_URL = 'http://localhost:5000/api';

const handleResponse = async (response) => {
    const contentType = response.headers.get("content-type");
    if (!response.ok) {
        let errorMessage = 'API request failed';
        if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            errorMessage = errorData.error || errorMessage;
        } else {
            errorMessage = await response.text() || errorMessage;
        }
        throw new Error(errorMessage);
    }
    return contentType && contentType.includes("application/json")
        ? response.json()
        : response.text();
};

const validateCoordinates = ({ latitude, longitude }) => {
    // Convert to numbers if they are strings
    const lat = typeof latitude === 'string' ? parseFloat(latitude) : latitude;
    const lng = typeof longitude === 'string' ? parseFloat(longitude) : longitude;

    // Check if conversion was successful
    if (isNaN(lat) || isNaN(lng)) {
        throw new Error('Latitude and longitude must be valid numbers');
    }

    // Validate latitude range
    if (lat < -90 || lat > 90) {
        throw new Error('Latitude must be between -90 and 90 degrees');
    }

    // Validate longitude range
    if (lng < -180 || lng > 180) {
        throw new Error('Longitude must be between -180 and 180 degrees');
    }

    return { latitude: lat, longitude: lng };
};

const apiService = {
    // Disaster CRUD operations
    getDisasters: async () => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

    getDisasterById: async (id) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

    createDisaster: async (disasterData) => {
        const response = await fetch(`${BASE_URL}/disasters/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(disasterData)
        });
        return handleResponse(response);
    },

    updateDisaster: async (id, disasterData) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(disasterData)
        });
        return handleResponse(response);
    },

    deleteDisaster: async (id) => {
        const response = await fetch(`${BASE_URL}/disasters/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        return handleResponse(response);
    },

    // Prediction operations
    getPrediction: async ({ latitude, longitude, location = '' }) => {
        try {
            // Validate and parse coordinates
            const validCoords = validateCoordinates({ latitude, longitude });

            const response = await fetch(`${BASE_URL}/predictions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    coordinates: validCoords,
                    location: location,
                    // Include specific parameters
                    rainfall: 0.8,  // You might want to fetch actual weather data
                    temperature: 23.0
                })
            });

            const data = await handleResponse(response);
            return {
                ...data,
                location: location,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error('Prediction API Error:', error);
            throw new Error(`Failed to get prediction: ${error.message}`);
        }
    },


    // frontend/src/services/api_service.js
    getDisasterDetails : async ({ lat, lng, query = '' }) => {
    try {
        // Validate coordinates if provided
        if (lat && lng) {
            validateCoordinates({
                latitude: parseFloat(lat),
                longitude: parseFloat(lng)
            });
        }

        const params = new URLSearchParams({
            lat: lat || '',
            lng: lng || '',
            query: query
        });

        const response = await fetch(`${BASE_URL}/disaster-details?${params}`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        return handleResponse(response);
    } catch (error) {
        console.error('Disaster Details API Error:', error);
        throw error;
    }
},
};

export default apiService;