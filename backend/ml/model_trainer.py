import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle


class ModelTrainer:
    def __init__(self, data_path, model_output_path, scaler_output_path):
        """
        Initialize the ModelTrainer with the paths for the data and output models.
        :param data_path: Path to the dataset (CSV)
        :param model_output_path: Path to save the trained model
        :param scaler_output_path: Path to save the trained scaler
        """
        self.data_path = data_path
        self.model_output_path = model_output_path
        self.scaler_output_path = scaler_output_path
        self.model = None
        self.scaler = None

    def load_data(self):
        """
        Loads and preprocesses the dataset from the given data path.
        :return: Preprocessed features and labels.
        """
        try:
            # Load the data
            data = pd.read_csv(self.data_path)
            print("Data loaded successfully.")

            # Assume the target column is 'disaster', adjust this as per your dataset
            X = data.drop('disaster', axis=1)  # Features
            y = data['disaster']  # Target variable (0 or 1)

            return X, y
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None, None

    def preprocess_data(self, X):
        """
        Scales the feature data using StandardScaler.
        :param X: Feature data to be scaled
        :return: Scaled features
        """
        try:
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            print("Data scaled successfully.")
            return X_scaled
        except Exception as e:
            print(f"Error during data preprocessing: {str(e)}")
            return None

    def train_model(self, X_train, y_train):
        """
        Trains a Random Forest model on the training data.
        :param X_train: Training features
        :param y_train: Training labels
        :return: Trained model
        """
        try:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            print("Model trained successfully.")
            return self.model
        except Exception as e:
            print(f"Error training the model: {str(e)}")
            return None

    def evaluate_model(self, X_test, y_test):
        """
        Evaluates the trained model on the test data.
        :param X_test: Test features
        :param y_test: Test labels
        :return: None (Prints the classification report)
        """
        try:
            y_pred = self.model.predict(X_test)
            print("Model evaluation:\n", classification_report(y_test, y_pred))
        except Exception as e:
            print(f"Error evaluating the model: {str(e)}")

    def save_model(self):
        """
        Saves the trained model and scaler to disk.
        :return: None
        """
        try:
            with open(self.model_output_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_output_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print("Model and scaler saved successfully.")
        except Exception as e:
            print(f"Error saving model or scaler: {str(e)}")

    def run(self):
        """
        Run the entire pipeline to train and save the model.
        :return: None
        """
        # Load and preprocess data
        X, y = self.load_data()
        if X is None or y is None:
            print("Exiting due to data loading error.")
            return

        X_scaled = self.preprocess_data(X)
        if X_scaled is None:
            print("Exiting due to preprocessing error.")
            return

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Train model
        self.train_model(X_train, y_train)

        # Evaluate model
        self.evaluate_model(X_test, y_test)

        # Save the model and scaler
        self.save_model()

