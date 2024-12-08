import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from backend.ml.models.disaster_predictor import DisasterPredictor

def train_model(data_path):
    """Train the disaster prediction model with historical data."""
    data = pd.read_csv(data_path)
    print("Columns in the dataset:")
    print(data.columns.tolist())

    # Choose an appropriate target variable
    target_variable = 'Disaster Type'  # Update this based on your data

    # Ensure the target variable exists in the data
    if target_variable not in data.columns:
        raise ValueError(f"'{target_variable}' column not found in the dataset.")

    # Separate features and target
    X = data.drop(columns=[target_variable])
    y = data[target_variable]

    # Handle missing values (if any)
    X = X.fillna(method='ffill')
    X = X.fillna(method='bfill')
    y = y.fillna(method='ffill')
    y = y.fillna(method='bfill')

    # Encode categorical variables
    from sklearn.preprocessing import LabelEncoder

    label_encoders = {}
    for column in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column].astype(str))
        label_encoders[column] = le

    # Encode the target variable if it's categorical
    y_le = LabelEncoder()
    y = y_le.fit_transform(y.astype(str))

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the model
    predictor = DisasterPredictor()
    predictor.train(X_train, y_train)

    # Evaluate model
    y_pred = predictor.model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model trained with accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    data_path = 'data/raw/disaster_historical_data.csv'  # Update with your CSV file path
    train_model(data_path)