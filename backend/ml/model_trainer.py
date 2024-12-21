import os
import sys
import pandas as pd
import numpy as np
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
VALID_DISASTER_TYPES = ['Earthquake', 'Flood', 'Cyclone', 'Drought']

def find_nearest_weather(disaster_row, weather_data, max_distance=1.0):
    """Find the nearest weather data point for a given disaster location."""
    distances = np.sqrt(
        (weather_data['latitude'].astype(float) - float(disaster_row['latitude'])) ** 2 +
        (weather_data['longitude'].astype(float) - float(disaster_row['longitude'])) ** 2
    )
    nearest_idx = distances.idxmin()
    min_distance = distances[nearest_idx]

    if min_distance <= max_distance:
        return weather_data.iloc[nearest_idx]
    return None


def preprocess_numeric_columns(df, columns):
    """Convert columns to numeric, handling any non-numeric values."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def train_model(data_path_1, data_path_2):
    """Train the disaster prediction model with historical and weather data."""
    try:
        # Load datasets
        logging.info("Loading datasets...")
        disaster_data = pd.read_csv(data_path_1)
        weather_data = pd.read_csv(data_path_2)

        # Convert coordinate columns to numeric
        numeric_columns = ['latitude', 'longitude', 'rainfall', 'temperature',
                           'pressure_mb', 'humidity', 'wind_kph', 'temperature_celsius',
                           'pressure_in']

        disaster_data = preprocess_numeric_columns(disaster_data, numeric_columns)
        weather_data = preprocess_numeric_columns(weather_data, numeric_columns)

        # Clean coordinates
        logging.info("Cleaning coordinate data...")
        disaster_data = disaster_data.dropna(subset=['latitude', 'longitude'])
        weather_data = weather_data.dropna(subset=['latitude', 'longitude'])

        # Log dataset shapes after cleaning
        logging.info(f"Disaster data shape after cleaning: {disaster_data.shape}")
        logging.info(f"Weather data shape after cleaning: {weather_data.shape}")

        # Round coordinates
        disaster_data['latitude'] = disaster_data['latitude'].round(2)
        disaster_data['longitude'] = disaster_data['longitude'].round(2)
        weather_data['latitude'] = weather_data['latitude'].round(2)
        weather_data['longitude'] = weather_data['longitude'].round(2)

        # Analyze coordinates in both datasets
        analyze_coordinates(disaster_data, "Disaster data")
        analyze_coordinates(weather_data, "Weather data")

        # Find nearest weather data for each disaster
        logging.info("Finding nearest weather data points...")
        matched_data = []

        for idx, disaster_row in disaster_data.iterrows():
            if idx % 1000 == 0:
                logging.info(f"Processing disaster record {idx}/{len(disaster_data)}")

            nearest_weather = find_nearest_weather(disaster_row, weather_data)
            if nearest_weather is not None:
                combined_row = {**disaster_row.to_dict(), **nearest_weather.to_dict()}
                matched_data.append(combined_row)

        # Create merged dataset
        data = pd.DataFrame(matched_data)
        logging.info(f"Shape after matching: {data.shape}")

        if data.shape[0] == 0:
            raise ValueError("No matching coordinates found even with approximate matching")

        # Select features
        features = ['latitude', 'longitude']
        weather_features = ['rainfall', 'temperature', 'pressure_mb', 'humidity',
                            'wind_kph', 'temperature_celsius', 'pressure_in']

        # Add available weather features
        features.extend([f for f in weather_features if f in data.columns])
        logging.info(f"Selected features: {features}")

        # Handle missing values
        logging.info("Checking and filling missing values...")
        X = data[features]
        X = X.apply(pd.to_numeric, errors='coerce')
        X = X.fillna(X.mean())

        # Prepare target variable and encode labels
        label_encoder = LabelEncoder()
        label_encoder.fit(VALID_DISASTER_TYPES)

        # Map disaster types to valid categories
        data['disaster_occurred'] = data['disaster_occurred'].apply(
            lambda x: x if x in VALID_DISASTER_TYPES else VALID_DISASTER_TYPES[0]
        )

        # Transform labels
        y = label_encoder.transform(data['disaster_occurred']) # Label encoding for target

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"\nModel Accuracy: {accuracy:.4f}")
        logging.info("\nClassification Report:")
        logging.info(classification_report(y_test, y_pred))

        joblib.dump(label_encoder, 'backend/ml/models/trained/label_encoder.pkl')

        return model, scaler, label_encoder

    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")
        raise


def analyze_coordinates(df, name):
    """Analyze coordinate ranges in a dataset."""
    logging.info(f"\n{name} coordinates analysis:")
    logging.info(f"Latitude range: {df['latitude'].min():.4f} to {df['latitude'].max():.4f}")
    logging.info(f"Longitude range: {df['longitude'].min():.4f} to {df['longitude'].max():.4f}")
    logging.info(f"Number of unique coordinates: {df.groupby(['latitude', 'longitude']).size().shape[0]}")


def validate_paths(data_path_1, data_path_2):
    """Validate the existence of input data files."""
    if not os.path.exists(data_path_1):
        logging.error(f"Error: Data file not found at {data_path_1}")
        return False
    if not os.path.exists(data_path_2):
        logging.error(f"Error: Data file not found at {data_path_2}")
        return False
    return True


if __name__ == "__main__":
    data_path_1 = '/Users/deepthanshm/PycharmProjects/disaster-management-system/data/raw/disaster_historical_data_updated.csv'
    data_path_2 = '/Users/deepthanshm/PycharmProjects/disaster-management-system/data/raw/GlobalWeatherRepository.csv'

    if not validate_paths(data_path_1, data_path_2):
        sys.exit(1)

    try:
        model, scaler, label_encoder = train_model(data_path_1, data_path_2)
        logging.info("Model training completed successfully!")
    except Exception as e:
        logging.error(f"Model training failed: {str(e)}")
        sys.exit(1)
