from sklearn.metrics import accuracy_score, mean_squared_error

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    return {"accuracy": accuracy, "mse": mse}
