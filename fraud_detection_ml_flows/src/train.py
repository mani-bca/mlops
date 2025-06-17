import mlflow
import mlflow.sklearn
import joblib
import os
from sklearn.linear_model import LogisticRegression
from src.evaluate import evaluate_model

def train_model(X_train, X_test, y_train, y_test, scaler, logger, model_output_dir="/tmp/models/"):
    # ✅ Ensure model output directory exists
    os.makedirs(model_output_dir, exist_ok=True)

    # ✅ Set MLflow tracking URI to a writable directory in Lambda
    mlflow.set_tracking_uri("file:/tmp/mlruns")

    # ✅ Set experiment explicitly to avoid default creation in read-only path
    mlflow.set_experiment("fraud_detection")

    with mlflow.start_run():
        model = LogisticRegression()
        model.fit(X_train, y_train)

        logger.info("Model training complete.")

        # Evaluate
        metrics = evaluate_model(model, X_test, y_test, logger)

        # Save locally
        model_path = os.path.join(model_output_dir, "fraud_model.pkl")
        scaler_path = os.path.join(model_output_dir, "scaler.pkl")
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        logger.info("Model and scaler saved to disk.")

        # Log with MLflow
        mlflow.sklearn.log_model(model, "sklearn-model")
        mlflow.log_artifact(model_path, artifact_path="model")
        mlflow.log_artifact(scaler_path, artifact_path="scaler")
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        logger.info("Model and scaler logged to MLflow.")
