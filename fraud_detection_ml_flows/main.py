import io
import json
from src.data_loader import load_csv_from_s3
from src.preprocess import preprocess_data
from src.train import train_model
from src.logger import get_logger

def main():
    log_stream = io.StringIO()
    logger = get_logger("fraud_detection", stream=log_stream)

    bucket_name = "lambda-code-bucket-ddd"
    object_key = "upload/transaction_samples.csv"

    logger.info("Starting fraud detection pipeline...")

    df = load_csv_from_s3(bucket_name, object_key)
    logger.info("Data loaded from S3.")

    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    logger.info("Data preprocessing complete.")

    train_model(X_train, X_test, y_train, y_test, scaler, logger)
    logger.info("Pipeline finished successfully.")

    # Return logs as Lambda output
    log_stream.seek(0)
    return {
        "statusCode": 200,
        "body": log_stream.read()
    }

def lambda_handler(event, context):
    return main()

if __name__ == "__main__":
    print(main())
