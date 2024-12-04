import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from backend.ml.models.disaster_predictor import DisasterPredictor

def train_model(data_path):
    """Train the disaster prediction model with historical data."""
    data = pd.read_csv(data_path)
    X = data.drop(columns=['disaster_occurred'])
    y = data['disaster_occurred']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    predictor = DisasterPredictor()
    predictor.train(X_train, y_train)

    # Evaluate model
    y_pred = predictor.model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model trained with accuracy: {accuracy:.2f}")
